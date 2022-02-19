from django.db import models


# Create your models here.

class ToolCategory(models.Model):
    name = models.CharField('网站分类名称', max_length=20)
    order_num = models.IntegerField('序号', default=99, help_text='序号可以用来调整顺序，越小越靠前')

    class Meta:
        verbose_name = '工具分类'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name

class ToolLink(models.Model):
    name = models.CharField('网站名称', max_length=20)
    description = models.CharField('网站描述', max_length=100)
    link = models.URLField('网站链接')
    order_num = models.IntegerField('序号', default=99, help_text='序号可以用来调整顺序，越小越靠前')
    category = models.ForeignKey(ToolCategory, verbose_name='网站分类',blank=True,null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '推荐工具'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name


class Exam(models.Model):
    objects = models.Manager()
    name = models.CharField('考试名称', max_length=50)
    level = models.CharField('考试等级', max_length=50)
    examtime = models.DateTimeField('考试日期')
    regist_date = models.DateTimeField('注册时间')
    signup_date = models.DateTimeField('报名时间')
    print_date = models.DateTimeField('打印准考证时间')
    create_date = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '考试安排'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

class ExamRemind(models.Model):
    user = models.CharField("用户", max_length=50)
    email = models.CharField("邮箱地址", max_length=128)
    which_exam = models.ForeignKey(Exam, related_name='remind_users', on_delete=models.CASCADE)