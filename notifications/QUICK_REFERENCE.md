# 🔔 Notifications System - Quick Reference Card

## ⚡ Quick Commands

```bash
# Start server
cd "c:\Users\techn\Desktop\dev\examplevibe\django projects"
python manage.py runserver

# Process notifications
python manage.py send_notifications --verbose

# Run tests
python manage.py test notifications

# Django shell
python manage.py shell
```

## 🌐 Quick URLs

| Page | URL |
|------|-----|
| **Notifications List** | `http://localhost:8000/notifications/` |
| **Admin** | `http://localhost:8000/admin/notifications/` |
| **Unread Count API** | `http://localhost:8000/notifications/api/unread-count/` |
| **Recent API** | `http://localhost:8000/notifications/api/recent/` |

## 📦 What's Included

```
✅ Notification Model           - Database storage
✅ Auto-Creation via Signals    - Automatic on event/appointment save
✅ Email Support                - Send email reminders
✅ Admin Interface              - Manage in Django admin
✅ User Views                   - /notifications/ page
✅ AJAX Endpoints               - For frontend integration
✅ Management Command           - Send pending notifications
✅ Email Template               - Beautiful HTML emails
✅ Full Test Suite              - 20+ tests
✅ Complete Documentation       - 5+ documentation files
```

## 🎯 Key Features at a Glance

| Feature | How It Works |
|---------|-------------|
| **Auto Notification** | Create Event → Auto-notify 1 hour before |
| **Appointment Notify** | Create Appointment → Auto-notify 2 hours before |
| **View Notifications** | Visit `/notifications/` page |
| **Mark Read** | Click notification or bulk action |
| **Email Reminders** | Configure email + run send command |
| **Delete** | Click delete button on notification |
| **Filter** | View: Unread, Pending, Read, All |

## 📱 Frontend Integration (Copy & Paste)

### Show Notification Bell
```html
<a href="{% url 'notifications:notification_list' %}">
    <i class="fas fa-bell"></i>
    <span class="badge" id="notif-count">0</span>
</a>

<script>
fetch('/notifications/api/unread-count/')
    .then(r => r.json())
    .then(d => {
        document.getElementById('notif-count').textContent = d.unread_count;
    });
</script>
```

### Recent Notifications Dropdown
```html
<div id="recent-notifications"></div>

<script>
fetch('/notifications/api/recent/')
    .then(r => r.json())
    .then(d => {
        let html = d.notifications.map(n => `
            <div class="notification-item">
                <strong>${n.title}</strong><br/>
                <small>${new Date(n.scheduled_time).toLocaleString()}</small>
            </div>
        `).join('');
        document.getElementById('recent-notifications').innerHTML = html;
    });
</script>
```

## 🔧 Configuration Checklist

- [ ] Verify 'notifications' in INSTALLED_APPS
- [ ] Verify notifications URLs added to urls.py
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create test event/appointment
- [ ] Run send_notifications command
- [ ] Check /notifications/ page
- [ ] (Optional) Configure email in settings.py
- [ ] (Optional) Set up scheduled execution

## 📊 Status Meanings

| Status | Meaning | Can Be |
|--------|---------|--------|
| **pending** | Created, waiting to send | Unread |
| **sent** | Successfully sent | Unread |
| **read** | User viewed it | Read |
| **failed** | Failed to send | Failed |

## 🐛 Quick Troubleshooting

**Q: Notifications not showing?**
- Check: Did you create an event/appointment?
- SQL: `SELECT * FROM notifications_notification;`

**Q: Notifications not created?**
- Restart server after migration
- Check signals: `apps.py` ready() method

**Q: Email not sending?**
- Run: `python manage.py send_notifications --verbose`
- Check: Email settings in settings.py
- Test: `python manage.py shell` then test email

**Q: Duplicate notifications?**
- Check: Event being saved twice
- Solution: Clear database and recreate

## 🗂️ File Organization

```
Core Logic:          models.py, signals.py, utils.py
Views & URLs:        views.py, urls.py
Templates:           templates/notifications/
Admin:               admin.py
Database:           migrations/
Testing:            tests.py
Commands:           management/commands/
Docs:               README.md, SETUP.md, EXAMPLES.py
```

## ✨ Usage Patterns

### In Templates
```html
{% for notif in pending_notifications %}
    <div>{{ notif.title }}</div>
    <p>{{ notif.message }}</p>
    <small>{{ notif.scheduled_time|date:"M d, Y" }}</small>
{% endfor %}
```

### In Views
```python
pending = Notification.objects.filter(
    user=request.user,
    status='pending'
).count()
```

### In Management Commands
```python
from notifications.utils import process_pending_notifications
sent, failed = process_pending_notifications()
print(f"Sent: {sent}, Failed: {failed}")
```

## 🎊 You're All Set!

Your notification system is **ready to use**. 

### Next Steps:
1. Create an event (visit `/events/create_event/`)
2. Watch notification appear automatically
3. Visit `/notifications/` to see it
4. Run `python manage.py send_notifications --verbose`
5. Configure email (optional)
6. Set up scheduled sending (optional)

### Documentation To Read:
- `README.md` - Full technical docs
- `SETUP.md` - Configuration guide
- `EXAMPLES.py` - Code examples
- `IMPLEMENTATION_SUMMARY.md` - Complete overview

---

## 📞 Quick Help

| Need | File |
|------|------|
| **Setup help** | SETUP.md |
| **Code examples** | EXAMPLES.py |
| **Full details** | README.md |
| **How it works** | IMPLEMENTATION_SUMMARY.md |
| **File list** | FILE_INDEX.md |

---

**Happy notifying! 🎉**
