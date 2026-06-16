# 🔐 إعدادات البوت - Bot Configuration

# معرف البوت
TOKEN = '8618726644:AAETMT6Ud1SEo4j6yjpFjtxSIpQisEJIBp8'

# معرفات المشرفين
ADMIN_IDS = [7320293829]  # @hashem_alkhaled203

# معلومات القناة
CHANNEL_USERNAME = 'Information_engineering_hashem'
CHANNEL_ID = None  # سيتم تحديثه تلقائياً

# قاعدة البيانات
DATABASE_PATH = 'university_bot.db'

# إعدادات التذكيرات
REMINDER_CHECK_INTERVAL = 60  # التحقق كل دقيقة

# الرسائل
MESSAGES = {
    'start': '👋 مرحباً بك في بوت الجامعة!\n\nاختر من القائمة أدناه:',
    'not_member': '❌ عذراً! يجب عليك أن تكون عضواً في القناة أولاً.\n\nانضم إلى القناة: @{channel}',
    'admin_only': '🚫 هذا الأمر للمشرفين فقط!',
    'help': '''📚 **قائمة المساعدة**

/start - بدء البوت
/schedule - عرض الجدول الدراسي
/add_class - إضافة محاضرة (إداري)
/remove_class - حذف محاضرة (إداري)
/reminders - إدارة التذكيرات
/quiz - بدء مسابقة
/gpa - حساب المعدل
/help - المساعدة
'''
}

