"""
Management command to fix region data issues.

Strategy:
- Keep full name records (ID 158-281)
- Delete code-format records (ID 1-157)
- Fix country_code to ISO 3166-1 alpha-2
- Fill empty area fields
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.heritage.models import HeritageItem
from apps.regions.models import Region


# ISO 3166-1 alpha-2 code mapping
ISO_3166_ALPHA2_MAP = {
    'afghanistan': 'AF', 'albania': 'AL', 'algeria': 'DZ', 'andorra': 'AD',
    'angola': 'AO', 'argentina': 'AR', 'armenia': 'AM', 'austria': 'AT',
    'azerbaijan': 'AZ', 'bahamas': 'BS', 'bahrain': 'BH', 'bangladesh': 'BD',
    'barbados': 'BB', 'belgium': 'BE', 'belize': 'BZ', 'benin': 'BJ',
    'bolivia': 'BO', 'bosnia and herzegovina': 'BA', 'botswana': 'BW',
    'brazil': 'BR', 'bulgaria': 'BG', 'burkina faso': 'BF', 'burundi': 'BI',
    'cambodia': 'KH', 'cameroon': 'CM', 'cape verde': 'CV',
    'central african republic': 'CF', 'chad': 'TD', 'chile': 'CL',
    'china': 'CN', 'colombia': 'CO', 'comoros': 'KM', 'congo': 'CG',
    'costa rica': 'CR', "cote d'ivoire": 'CI', 'croatia': 'HR', 'cuba': 'CU',
    'cyprus': 'CY', 'czech republic': 'CZ', 'denmark': 'DK', 'djibouti': 'DJ',
    'dominican republic': 'DO', 'ecuador': 'EC', 'egypt': 'EG', 'el salvador': 'SV',
    'estonia': 'EE', 'ethiopia': 'ET', 'fiji': 'FJ', 'finland': 'FI',
    'france': 'FR', 'gabon': 'GA', 'gambia': 'GM', 'georgia': 'GE',
    'germany': 'DE', 'ghana': 'GH', 'greece': 'GR', 'grenada': 'GD',
    'guatemala': 'GT', 'guinea': 'GN', 'haiti': 'HT', 'honduras': 'HN',
    'hungary': 'HU', 'iceland': 'IS', 'india': 'IN', 'indonesia': 'ID',
    'iran': 'IR', 'iraq': 'IQ', 'ireland': 'IE', 'israel': 'IL', 'italy': 'IT',
    'jamaica': 'JM', 'japan': 'JP', 'jordan': 'JO', 'kazakhstan': 'KZ',
    'kenya': 'KE', 'kuwait': 'KW', 'kyrgyzstan': 'KG', 'laos': 'LA',
    'latvia': 'LV', 'lebanon': 'LB', 'libya': 'LY', 'lithuania': 'LT',
    'luxembourg': 'LU', 'madagascar': 'MG', 'malawi': 'MW', 'malaysia': 'MY',
    'mali': 'ML', 'malta': 'MT', 'mauritania': 'MR', 'mauritius': 'MU',
    'mexico': 'MX', 'micronesia': 'FM', 'moldova': 'MD', 'mongolia': 'MN',
    'morocco': 'MA', 'myanmar': 'MM', 'namibia': 'NA', 'nepal': 'NP',
    'netherlands': 'NL', 'nicaragua': 'NI', 'niger': 'NE', 'nigeria': 'NG',
    'north korea': 'KP', 'norway': 'NO', 'oman': 'OM', 'pakistan': 'PK',
    'panama': 'PA', 'paraguay': 'PY', 'peru': 'PE', 'philippines': 'PH',
    'poland': 'PL', 'portugal': 'PT', 'qatar': 'QA', 'romania': 'RO',
    'russia': 'RU', 'rwanda': 'RW', 'saudi arabia': 'SA', 'senegal': 'SN',
    'serbia': 'RS', 'singapore': 'SG', 'slovakia': 'SK', 'slovenia': 'SI',
    'somalia': 'SO', 'south korea': 'KR', 'spain': 'ES', 'sri lanka': 'LK',
    'sudan': 'SD', 'sweden': 'SE', 'switzerland': 'CH', 'syria': 'SY',
    'tajikistan': 'TJ', 'tanzania': 'TZ', 'thailand': 'TH', 'timor-leste': 'TL',
    'togo': 'TG', 'tunisia': 'TN', 'turkey': 'TR', 'turkmenistan': 'TM',
    'uganda': 'UG', 'ukraine': 'UA', 'united arab emirates': 'AE',
    'united kingdom': 'GB', 'united states': 'US', 'uruguay': 'UY',
    'uzbekistan': 'UZ', 'venezuela': 'VE', 'vietnam': 'VN', 'yemen': 'YE',
    'zambia': 'ZM', 'zimbabwe': 'ZW',
}


class Command(BaseCommand):
    help = 'Fix region data and fill empty area fields with country names'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--fix-areas', action='store_true')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fix_areas = options['fix_areas']

        self.stdout.write('=' * 60)
        self.stdout.write('Region Data Fix Command')
        self.stdout.write('=' * 60)
        self.stdout.write(f'Dry run: {dry_run}, Fix areas: {fix_areas}')
        self.stdout.write('')

        with transaction.atomic():
            # Step 1: Find code-format regions (ID 1-157)
            self.stdout.write('Step 1: Finding code-format regions...')
            code_regions = Region.objects.filter(
                id__lte=157
            ).order_by('id')
            self.stdout.write(f'  Found {code_regions.count()} code-format regions')
            self.stdout.write('')

            # Step 2: Build code to region mapping for full-name regions
            self.stdout.write('Step 2: Building full-name region mapping...')
            full_regions = Region.objects.filter(
                id__gt=157
            )
            code_to_region = {}  # {alpha2_code: region_id}

            for region in full_regions:
                name_lower = region.country_name.lower().strip()
                correct_code = ISO_3166_ALPHA2_MAP.get(name_lower)
                if correct_code:
                    code_to_region[correct_code] = region.id

            self.stdout.write(f'  Mapped {len(code_to_region)} full-name regions to codes')
            self.stdout.write('')

            # Step 3: Build mapping and reassign
            self.stdout.write('Step 3: Reassigning heritage items...')
            total_reassigned = 0
            to_delete = []

            for code_region in code_regions:
                code = code_region.country_code.upper()
                if code in code_to_region:
                    full_id = code_to_region[code]
                    count = HeritageItem.objects.filter(region_id=code_region.id).count()
                    if count > 0:
                        if not dry_run:
                            HeritageItem.objects.filter(region_id=code_region.id).update(region_id=full_id)
                        total_reassigned += count
                    to_delete.append(code_region.id)

            self.stdout.write(f'  Total items reassigned: {total_reassigned}')
            self.stdout.write(f'  Regions to delete: {len(to_delete)}')
            self.stdout.write('')

            # Step 4: Delete code-format regions
            self.stdout.write('Step 4: Deleting code-format regions...')
            if not dry_run:
                deleted = Region.objects.filter(id__in=to_delete).delete()[0]
                self.stdout.write(f'  Deleted {deleted} code-format regions')
            else:
                self.stdout.write(f'  Would delete {len(to_delete)} regions')
            self.stdout.write('')

            # Step 5: Fix country codes
            self.stdout.write('Step 5: Fixing country codes...')
            fixed_count = 0
            for region in Region.objects.all():
                name_lower = region.country_name.lower().strip()
                correct_code = ISO_3166_ALPHA2_MAP.get(name_lower)
                if correct_code and region.country_code.upper() != correct_code:
                    old_code = region.country_code
                    if not dry_run:
                        region.country_code = correct_code
                        region.save()
                    fixed_count += 1
                    if fixed_count <= 5:
                        self.stdout.write(f'  {region.country_name}: {old_code} -> {correct_code}')

            self.stdout.write(f'  Total codes fixed: {fixed_count}')
            self.stdout.write('')

            # Step 6: Fix empty areas
            if fix_areas:
                self.stdout.write('Step 6: Fixing empty area fields...')
                empty_area_items = HeritageItem.objects.filter(area='').select_related('region')
                area_count = empty_area_items.count()
                self.stdout.write(f'  Empty area records: {area_count}')

                if not dry_run:
                    updated = 0
                    for item in empty_area_items:
                        if item.region:
                            item.area = item.region.country_name
                            item.save(update_fields=['area'])
                            updated += 1
                    self.stdout.write(f'  Updated {updated} records')
                else:
                    self.stdout.write(f'  Would update {area_count} records')
                self.stdout.write('')

            # Summary
            final_count = Region.objects.count()
            self.stdout.write('=' * 60)
            self.stdout.write(f'Summary: {final_count} regions remaining, {total_reassigned} items reassigned')

            if dry_run:
                self.stdout.write('DRY RUN - No changes made')
                raise Exception('Dry run rollback')
            else:
                self.stdout.write('SUCCESS - All fixes applied!')
