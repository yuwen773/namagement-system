"""
Django Management Command: 使用 AI 生成回答

使用方法:
    python manage.py generate_answers                    # 开始生成
    python manage.py generate_answers --resume           # 继续中断的任务
    python manage.py generate_answers --limit=100        # 只生成100个
    python manage.py generate_answers --status           # 查看进度
"""
import os
import sys
import time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.crawler.models import Question, Answer, AnswerGenerationProgress
from apps.crawler.management.utils.ai_answer_generator import AIAnswerGenerator


class Command(BaseCommand):
    help = '使用 AI 为问题生成回答'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_progress_length = 0

    def add_arguments(self, parser):
        """添加命令行参数"""
        parser.add_argument(
            '--api-key',
            type=str,
            default='sk-gfxO1Z54MHXNce9LDoIcMJVPpSbqLOxagWtHok76cqsu8RBi',
            help='DMXAPI API Key'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='限制生成的回答数量'
        )
        parser.add_argument(
            '--resume',
            action='store_true',
            help='继续上一次中断的任务'
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='查看当前进度状态'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='重置所有进度（慎用）'
        )

    def handle(self, *args, **options):
        """命令处理逻辑"""
        api_key = options['api_key']
        limit = options['limit']
        resume = options['resume']
        show_status = options['status']
        reset = options['reset']

        # 查看状态
        if show_status:
            self._show_status()
            return

        # 重置进度
        if reset:
            self._reset_progress()
            return

        # 执行生成
        self._run_generation(api_key, limit, resume)

    def _show_status(self):
        """显示当前状态"""
        from apps.crawler.models import Question, Answer

        total_questions = Question.objects.count()
        questions_with_answers = Question.objects.filter(answers__isnull=False).distinct().count()
        questions_without_answers = total_questions - questions_with_answers

        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("回答生成状态"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(f"  总问题数: {total_questions}")
        self.stdout.write(f"  已有回答: {questions_with_answers}")
        self.stdout.write(f"  缺少回答: {questions_without_answers}")
        self.stdout.write(f"  回答总数: {Answer.objects.count()}")
        self.stdout.write("")

        # 显示进度任务
        progress = AnswerGenerationProgress.objects.filter(
            status__in=['running', 'paused']
        ).order_by('-created_at').first()

        if progress:
            self.stdout.write(self.style.SUCCESS(f"当前任务: {progress.task_id}"))
            self.stdout.write(f"  状态: {progress.get_status_display()}")
            self.stdout.write(f"  进度: {progress.completed}/{progress.total} ({progress.progress_percent}%)")
            self.stdout.write(f"  成功: {progress.completed} | 失败: {progress.failed} | 跳过: {progress.skipped}")
            if progress.last_question_id:
                self.stdout.write(f"  最后处理: {progress.last_question_id}")
        else:
            self.stdout.write("  没有运行中的任务")

    def _reset_progress(self):
        """重置进度"""
        confirm = input("确认要重置所有进度吗？这将标记所有任务为已完成 (yes/no): ")
        if confirm.lower() == 'yes':
            count = AnswerGenerationProgress.objects.filter(
                status__in=['running', 'paused']
            ).update(status='paused')
            self.stdout.write(self.style.SUCCESS(f"已重置 {count} 个任务"))
        else:
            self.stdout.write("取消操作")

    def _run_generation(self, api_key: str, limit: int, resume: bool):
        """执行回答生成"""
        # 打印配置信息
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("AI 回答生成工具"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(f"API: DMXAPI (GLM-4.7-Flash)")
        self.stdout.write(f"模式: {'继续任务' if resume else '新建任务'}")
        if limit:
            self.stdout.write(f"限制数量: {limit}")
        self.stdout.write("")

        # 创建生成器
        generator = AIAnswerGenerator(api_key)

        # 获取问题列表
        start_from_id = None
        if resume:
            progress = generator.get_latest_progress()
            if progress:
                start_from_id = progress.last_question_id
                self.stdout.write(f"继续任务: {progress.task_id}")
                self.stdout.write(f"从问题 ID: {start_from_id} 开始")
                self.stdout.write("")
            else:
                self.stdout.write(self.style.WARNING("没有找到可继续的任务，将创建新任务"))
                resume = False

        questions = generator.get_questions_without_answers(
            limit=limit,
            start_from_id=start_from_id
        )

        if not questions:
            self.stdout.write(self.style.SUCCESS("所有问题都已有回答！"))
            return

        self.stdout.write(f"找到 {len(questions)} 个需要生成回答的问题")
        self.stdout.write("")

        # 创建或更新进度任务
        if not resume or not generator.get_latest_progress():
            # 获取总数
            total = Question.objects.filter(answers__isnull=True).count()
            progress = generator.create_progress_task(total)
            self.stdout.write(f"创建任务: {progress.task_id}")
        else:
            progress = generator.get_latest_progress()

        # 开始生成
        start_time = time.time()

        result = generator.generate_batch(
            questions=questions,
            progress=progress,
            progress_callback=self._progress_callback
        )

        elapsed_time = time.time() - start_time

        # 清除进度行
        self._clear_progress()

        # 更新任务状态
        progress.status = 'completed'
        progress.save(update_fields=['status', 'updated_at'])

        # 打印结果
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("生成完成"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(f"  总计: {result['total']} 条")
        self.stdout.write(self.style.SUCCESS(f"  成功: {result['success']} 条"))
        if result['failed'] > 0:
            self.stdout.write(self.style.ERROR(f"  失败: {result['failed']} 条"))
        if result['skipped'] > 0:
            self.stdout.write(self.style.WARNING(f"  跳过: {result['skipped']} 条"))
        self.stdout.write(f"  耗时: {elapsed_time:.2f} 秒")
        self.stdout.write(f"  平均: {elapsed_time / result['total']:.2f} 秒/条")

    def _progress_callback(self, current: int, total: int, result: dict, question):
        """进度回调函数"""
        progress = int((current / total) * 100) if total > 0 else 0
        bar_length = 50
        filled = int((progress / 100) * bar_length)
        bar = '=' * filled + '>' + ' ' * (bar_length - filled - 1) if filled < bar_length else '=' * bar_length

        # 构建进度行
        progress_line = (
            f"\r[{bar}] {progress:3}% ({current}/{total}) | "
            f"成功: {result['success']} | "
            f"失败: {result['failed']} | "
            f"跳过: {result['skipped']}"
        )

        # 输出进度
        self.stdout.write(progress_line, ending='')
        self.stdout.flush()

        self.last_progress_length = len(progress_line)

    def _clear_progress(self):
        """清除进度行"""
        if self.last_progress_length > 0:
            self.stdout.write('\r' + ' ' * self.last_progress_length + '\r', ending='')
            self.stdout.flush()
