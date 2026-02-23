"""
AI 回答生成工具类

使用 DMXAPI 调用 GLM-4.7-Flash 模型为问题生成回答。
"""
import json
import time
import uuid
from typing import Dict, List, Optional, Callable
from datetime import datetime

import requests

from django.conf import settings
from django.db import transaction

from apps.crawler.models import Question, Answer, AnswerGenerationProgress


class AIAnswerGenerator:
    """AI 回答生成器"""

    # DMXAPI 配置
    API_BASE_URL = "https://www.dmxapi.cn"
    API_PATH = "/v1/chat/completions"
    MODEL = "GLM-4.7-Flash"

    # Prompt 模板
    SYSTEM_PROMPT = "简洁回答，一句话就行。"

    def __init__(self, api_key: str):
        """
        初始化生成器

        Args:
            api_key: DMXAPI API Key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'DMXAPI/1.0.0',
            'Content-Type': 'application/json'
        })

    def generate_answer(self, question: Question) -> Optional[str]:
        """
        为单个问题生成回答

        Args:
            question: 问题对象

        Returns:
            生成的回答内容，失败返回 None
        """
        try:
            # 构建用户消息 - 简洁明了
            user_content = f"{question.title}（用一句话回答，不超过50字）"

            # 构建请求
            payload = {
                "model": self.MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_content
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 150
            }

            # 发送请求
            url = f"{self.API_BASE_URL}{self.API_PATH}"
            response = self.session.post(
                url,
                json=payload,
                timeout=30
            )

            # 检查响应
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    message = data['choices'][0]['message']
                    # 优先使用 content，如果为空则尝试 reasoning_content
                    answer = message.get('content', '').strip()
                    if not answer:
                        answer = message.get('reasoning_content', '').strip()
                    if answer:
                        return answer
                    else:
                        print(f"API 响应中无内容: {data}")
                        return None
                else:
                    print(f"API 响应格式错误: {data}")
                    return None
            else:
                print(f"API 请求失败: {response.status_code} - {response.text}")
                return None

        except requests.Timeout:
            print(f"API 请求超时: {question.question_id}")
            return None
        except Exception as e:
            print(f"生成回答时出错: {e}")
            return None

    def save_answer(self, question: Question, content: str) -> Answer:
        """
        保存生成的回答

        Args:
            question: 问题对象
            content: 回答内容

        Returns:
            Answer 对象
        """
        # 获取当前最大 order
        max_order = Answer.objects.filter(
            question=question
        ).aggregate(max_order=models.Max('source_order'))['max_order'] or 0

        # 创建回答
        answer = Answer.objects.create(
            question=question,
            content=content,
            answerer='AI助手',
            source_order=max_order + 1,
            is_ai_generated=True,
            answer_time=datetime.now()
        )

        return answer

    def get_questions_without_answers(self, limit: Optional[int] = None,
                                     start_from_id: Optional[str] = None) -> List[Question]:
        """
        获取没有回答的问题

        Args:
            limit: 限制数量
            start_from_id: 从指定问题ID开始（用于断点续传）

        Returns:
            问题列表
        """
        # 获取没有回答的问题
        questions = Question.objects.filter(
            answers__isnull=True
        ).order_by('question_id')

        if start_from_id:
            questions = questions.filter(question_id__gte=start_from_id)

        if limit:
            questions = questions[:limit]

        return list(questions)

    def generate_batch(
        self,
        questions: List[Question],
        progress: Optional[AnswerGenerationProgress] = None,
        progress_callback: Optional[Callable] = None
    ) -> Dict:
        """
        批量生成回答

        Args:
            questions: 问题列表
            progress: 进度对象
            progress_callback: 进度回调函数

        Returns:
            结果统计字典
        """
        result = {
            'total': len(questions),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }

        for i, question in enumerate(questions):
            try:
                # 生成回答
                answer_content = self.generate_answer(question)

                if answer_content:
                    # 保存回答
                    self.save_answer(question, answer_content)
                    result['success'] += 1

                    # 更新进度
                    if progress:
                        progress.completed += 1
                        progress.last_question_id = question.question_id
                        progress.save(update_fields=['completed', 'last_question_id', 'updated_at'])
                else:
                    result['failed'] += 1
                    if progress:
                        progress.failed += 1
                        progress.save(update_fields=['failed', 'updated_at'])

                # 进度回调
                if progress_callback:
                    progress_callback(i + 1, len(questions), result, question)

                # 避免触发限流，稍微延迟
                time.sleep(2)

            except Exception as e:
                print(f"处理问题 {question.question_id} 时出错: {e}")
                result['failed'] += 1
                if progress:
                    progress.failed += 1
                    progress.save(update_fields=['failed', 'updated_at'])

        return result

    def create_progress_task(self, total: int) -> AnswerGenerationProgress:
        """
        创建进度追踪任务

        Args:
            total: 总问题数

        Returns:
            AnswerGenerationProgress 对象
        """
        task_id = str(uuid.uuid4())[:8]
        progress = AnswerGenerationProgress.objects.create(
            task_id=task_id,
            total=total,
            status='running'
        )
        return progress

    @staticmethod
    def get_latest_progress() -> Optional[AnswerGenerationProgress]:
        """获取最新的进度任务"""
        return AnswerGenerationProgress.objects.filter(
            status__in=['running', 'paused']
        ).order_by('-created_at').first()


# Django 导入
from django.db import models
