#encoding=utf-8

from django.test import TestCase
from molp.models import Parameter
from datetime import datetime
from datetime import timedelta


class ParameterManagerTestCase(TestCase):

    def test_app_only(self):
        """测试参数只指定app
        """
        p = Parameter(app='net.jf.test', name='name', value='jeff')
        p.save()
        p = Parameter(app='net.jf.test', name='gender', value='male')
        p.save()

        ps = Parameter.objects.get_parameters('net.jf.test', version='1.0',
                                              channel='appstroe')
        self.assertEqual(2, len(ps))

    def test_app_version_not_match(self):
        """定义具体版本号的参数，但请求不匹配。返回默认参数。
        """
        p = Parameter(app='net.jf.test', name='name', value='jeff')
        p.save()
        p = Parameter(app='net.jf.test', name='name', value='vera',
                      version='1.1')
        p.save()

        ps = Parameter.objects.get_parameters('net.jf.test', version='1.0',
                                              channel='appstroe')
        self.assertEqual(1, len(ps))
        self.assertEqual('jeff', ps[0].value)

    def test_app_version_match(self):
        """定义具体版本号的参数，请求亦匹配
        """
        p = Parameter(app='net.jf.test', name='name', value='jeff')
        p.save()
        p = Parameter(app='net.jf.test', name='name', value='vera',
                      version='1.1')
        p.save()

        ps = Parameter.objects.get_parameters('net.jf.test', version='1.1',
                                              channel='appstroe')
        self.assertEqual(1, len(ps))
        self.assertEqual('vera', ps[0].value)

    def test_match_not_complete(self):
        """部分参数匹配，但并非全匹配，视为不匹配。
        """
        p = Parameter(app='net.jf.test', name='name', value='jeff')
        p.save()
        p = Parameter(app='net.jf.test', name='name', value='vera',
                      version='1.1', channel='pp')
        p.save()

        ps = Parameter.objects.get_parameters('net.jf.test', version='1.1',
                                              channel='appstroe')
        self.assertEqual(1, len(ps))
        self.assertEqual('jeff', ps[0].value)

    def test_too_early_to_see(self):
        """参数定义生效时间，在生效前参数不可见。生效后可见。
        """
        p = Parameter(app='net.jf.test', name='name', value='jeff')
        p.save()
        p = Parameter(app='net.jf.test', name='gender', value='male',
                      version='1.1',
                      effect_time=datetime.now() + timedelta(days=1))
        p.save()

        ps = Parameter.objects.get_parameters('net.jf.test', version='1.1',
                                              channel='appstore',
                                              since=datetime.now())
        self.assertEqual(1, len(ps))
        self.assertEqual('name', ps[0].name)

        ps = Parameter.objects.get_parameters(
            'net.jf.test', version='1.1',
            channel='appstore',
            since=datetime.now() + timedelta(days=2))
        self.assertEqual(2, len(ps))
