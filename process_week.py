from datetime import datetime
from datetime import timedelta


class WeekTransformer:

    CONFIG = {
        'TIME_FORMAT': '%Y-%m-%d %H:%M:%S',
        'WEEK_OFFSET': timedelta(hours=24 + 24 + 6),

        'CITY_FIELD_ID': 512318,
        'DRUPAL_UTM_FIELD_ID': 632884,

        'TILDA_UTM_SOURCE_FIELD_ID': 648158,
        'TILDA_UTM_MEDIUM_FIELD_ID': 648160,
        'TILDA_UTM_CAMPAIGN_FIELD_ID': 648310,
        'TILDA_UTM_CONTENT_FIELD_ID': 648312,
        'TILDA_UTM_TERM_FIELD_ID': 648314,

        'CT_UTM_SOURCE_FIELD_ID': 648256,
        'CT_UTM_MEDIUM_FIELD_ID': 648258,
        'CT_UTM_CAMPAIGN_FIELD_ID': 648260,
        'CT_UTM_CONTENT_FIELD_ID': 648262,
        'CT_UTM_TERM_FIELD_ID': 648264,

        'CT_TYPE_COMMUNICATION_FIELD_ID': 648220,
        'CT_DEVICE_FIELD_ID': 648276,
        'CT_OS_FIELD_ID': 648278,
        'CT_BROWSER_FIELD_ID': 648280,
    }

    def __init__(self, config=None):
        self.CONFIG = dict()
        if config:
            self.CONFIG = config
        self.CONFIG.update(WeekTransformer.CONFIG)

        self.week_data = []

    def extract(self, file_path):
        pass

    def transform(self, data):
        result = []
        for row in self.week_data:
            result.append(
                self.transform_row(row))

    def transform_row(self, source_row):

        created_at_datetime = datetime.fromtimestamp(source_row['created_at'])

        result_row = {
            'id': source_row['id'],
            'created_at': source_row['created_at'],

            'amo_updated_at': (None if 'updated_by' not in source_row else
                               source_row['updated_by']),

            'amo_trashed_at': (None if 'trashed_at' not in source_row else
                               source_row['trashed_at']),

            'amo_closed_at': (None if 'closed_at' not in source_row else
                              source_row['closed_at']),

            'amo_status_id': source_row['status_id'],
            'amo_pipeline_id': source_row['pipeline_id'],

            'amo_city': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CITY_FIELD_ID']),

            'drupal_utm': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['DRUPAL_UTM_FIELD_ID']),

            'tilda_utm_source': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['TILDA_UTM_SOURCE_FIELD_ID']),

            'tilda_utm_medium': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['TILDA_UTM_MEDIUM_FIELD_ID']),

            'tilda_utm_campaign': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['TILDA_UTM_CAMPAIGN_FIELD_ID']),

            'tilda_utm_content': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['TILDA_UTM_CONTENT_FIELD_ID']),

            'tilda_utm_term': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['TILDA_UTM_TERM_FIELD_ID']),

            'ct_utm_source': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_UTM_SOURCE_FIELD_ID']),

            'ct_utm_medium': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_UTM_MEDIUM_FIELD_ID']),

            'ct_utm_campaign': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_UTM_CAMPAIGN_FIELD_ID']),

            'ct_utm_content': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_UTM_CONTENT_FIELD_ID']),

            'ct_utm_term': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_UTM_TERM_FIELD_ID']),

            'ct_type_communication': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_TYPE_COMMUNICATION_FIELD_ID']),

            'ct_device': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_DEVICE_FIELD_ID']),

            'ct_os': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_OS_FIELD_ID']),

            'ct_browser': self._get_custom_field_value_by_id(
                source_row, self.CONFIG['CT_BROWSER_FIELD_ID']),

            'created_at_bq_timestamp': created_at_datetime.strftime(
                self.CONFIG['TIME_FORMAT']),

            'created_at_year': created_at_datetime.year,
            'created_at_month': created_at_datetime.month,
            'created_at_week': ((created_at_datetime + self.CONFIG['WEEK_OFFSET'])
                                .isocalendar()[1])
        }

        self._check_utm()

        return result_row

    def _get_custom_field_value_by_id(self, source_row, field_id):
        if 'custom_fields_values' in source_row:
            for field in source_row['custom_fields_values']:
                if field['field_id'] == field_id:
                    return field['values'][0].get('value', None)

        return None

    def _get_lead_utm_source(self, result_row):

        if result_row['drupal_utm']:

            drupal_utm_list = result_row['drupal_utm'].split(', ')
            drupal_utm_dict = dict([
                item.split('=') for item in drupal_utm_list])

            if 'source' in drupal_utm_dict:
                return drupal_utm_dict['source']

            if 'medium' in drupal_utm_dict:
                if drupal_utm_dict['medium'] == 'yandex':
                    return 'yandex'

        if result_row['ct_utm_source']:
            return result_row['ct_utm_source']

        return result_row['tilda_utm_source']

    def _check_utm(self):
        pass

    def load(self):
        pass

