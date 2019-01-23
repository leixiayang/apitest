from django.db import models


# Create your models here.

class directorytree(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=254)
    key = models.CharField(max_length=100)
    level = models.IntegerField()
    project = models.ForeignKey(
        'interface_platform.project',
        on_delete=models.CASCADE,
        null=False
    )


class itbody(models.Model):
    name = models.CharField(max_length=100)
    body_format = models.SmallIntegerField()
    type = models.CharField(max_length=50)
    desc = models.CharField(max_length=254, null=True, default=None)
    value = models.TextField()
    upload_file = models.CharField(max_length=100, null=True, default=None)
    it = models.ForeignKey(
        'interface_platform.itstatement',
        on_delete=models.CASCADE,
        null=False
    )
    body_type = models.SmallIntegerField()


class itheader(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=254)
    type = models.CharField(max_length=10, null=True, default=None)
    desc = models.CharField(max_length=254, null=True, default=None)
    it = models.ForeignKey(
        'interface_platform.itstatement',
        on_delete=models.CASCADE,
        null=False
    )
    header_type = models.SmallIntegerField()


class itlog(models.Model):
    it = models.ForeignKey(
        'interface_platform.itstatement',
        on_delete=models.CASCADE,
        null=False
    )
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    log_path = models.CharField(max_length=254)


class itparam(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=254)
    type = models.CharField(max_length=10, null=True, default=None)
    it = models.ForeignKey(
        'interface_platform.itstatement',
        on_delete=models.CASCADE,
        null=False
    )


class itstatement(models.Model):
    name = models.CharField(max_length=100)
    protocol_type = models.CharField(max_length=10)
    request_type = models.CharField(max_length=10)
    path = models.CharField(max_length=100)
    desc = models.CharField(max_length=254, null=True, default=None)
    project = models.ForeignKey(
        'interface_platform.project',
        on_delete=models.CASCADE,
        null=False
    )
    creator = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )
    # host = models.ForeignKey(
    #     'interface_platform.variable',
    #     on_delete=models.CASCADE,
    #     null=False
    # )
    status = models.CharField(max_length=20)
    responsible = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        related_name='+',
        null=False
    )
    timestamp = models.DateTimeField()

    requestparam = models.CharField(max_length=100)

    expectres = models.CharField(max_length=100)


class project(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=254, null=True, default=None)
    user = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )


class tag(models.Model):
    name = models.CharField(max_length=254)
    num = models.IntegerField()


class tagmap(models.Model):
    tag = models.ForeignKey(
        'interface_platform.testcase',
        on_delete=models.CASCADE,
        null=False
    )
    tc = models.ForeignKey(
        'interface_platform.tag',
        on_delete=models.CASCADE,
        null=False
    )


class testcase(models.Model):
    name = models.CharField(max_length=254)
    belong = models.ForeignKey(
        'interface_platform.directorytree',
        on_delete=models.CASCADE,
        null=False
    )
    status = models.CharField(max_length=20)
    author = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )
    responsible = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        related_name='+',
        null=False
    )
    timestamp = models.DateTimeField()
    tags = models.CharField(max_length=254, null=True, default=None)


class testcaselog(models.Model):
    tc = models.ForeignKey(
        'interface_platform.testcase',
        on_delete=models.CASCADE,
        null=False
    )
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    log_path = models.CharField(max_length=254)


class testcasestep(models.Model):
    tc = models.ForeignKey(
        'interface_platform.testcase',
        on_delete=models.CASCADE,
        null=False
    )
    it = models.ForeignKey(
        'interface_platform.itstatement',
        on_delete=models.CASCADE,
        null=False
    )
    index = models.IntegerField()
    name = models.CharField(max_length=100)


class testsuite(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    runner = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )
    rerun = models.SmallIntegerField()
    testcase = models.ForeignKey(
        'interface_platform.testcase',
        on_delete=models.CASCADE,
        null=False
    )
    passednum = models.IntegerField()
    failednum = models.IntegerField()
    skippednum = models.IntegerField()


class testsuite_test_cases(models.Model):
    testsuite = models.ForeignKey(
        'interface_platform.testsuite',
        on_delete=models.CASCADE,
        null=False
    )
    testcase = models.ForeignKey(
        'interface_platform.testcase',
        on_delete=models.CASCADE,
        null=False
    )


class uniid(models.Model):
    tc = models.ForeignKey(
        'interface_platform.testcase',
        on_delete=models.CASCADE,
        default=None
    )
    it = models.ForeignKey(
        'interface_platform.itstatement',
        on_delete=models.CASCADE,
        default=None

    )
    test_suite = models.ForeignKey(
        'interface_platform.testsuite',
        on_delete=models.CASCADE,
        default=None

    )


class variable(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=254, null=True, default=None)
    value = models.CharField(max_length=254)
    project = models.ForeignKey(
        'interface_platform.project',
        on_delete=models.CASCADE,
        null=False
    )
    type = models.CharField(max_length=100)
    mark = models.CharField(max_length=100)
    creator = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        null=False
    )
    responsible = models.ForeignKey(
        'auth.user',
        on_delete=models.CASCADE,
        related_name='+',
        null=False
    )
    timestamp = models.DateTimeField()


class variableit(models.Model):
    var = models.ForeignKey(
        'interface_platform.variable',
        on_delete=models.CASCADE,
        null=False
    )
    it = models.ForeignKey(
        'interface_platform.itstatement',
        on_delete=models.CASCADE,
        null=False
    )
    assoc_type = models.CharField(max_length=100, null=True, default=None)
    assoc_id = models.IntegerField(null=True, default=None)
