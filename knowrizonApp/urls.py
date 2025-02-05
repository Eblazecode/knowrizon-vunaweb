from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin_dashboard/', views.admin_dasahboard, name='admin_dashboard'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_login/', views.admin_login, name='admin_login'),
    # path('student_registration/', views.student_register, name='student_register'),
    path('add_users/', views.add_user, name='add_users'),
    path('add_students/', views.add_student, name='add_students'),
    path('approve_requests/', views.approve_requests, name='approve_requests'),
    path('manage_user_roles/', views.manage_user_roles, name='manage_user_roles'),
    path('handle_password_resets/', views.handle_password_resets, name='handle_password_resets'),
    path('monitor_user_activity/', views.monitor_user_activity, name='monitor_user_activity'),
    path('oversee_user_permissions/', views.oversee_user_permissions, name='oversee_user_permissions'),
    path('add_academic_staff/', views.add_academic_staff, name='add_academic_staff'),
    path('add_content_manager/', views.add_content_manager, name='add_content_manager'),
    path('library_materials_category/', views.library_materials_category, name='library_materials_category'),
    path('upload_students_records/', views.upload_students_records, name='upload_students_records'),
    path('process_bulk_student_upload/', views.bulk_upload_students, name='process_bulk_student_upload'),
    path('upload_staff_records/', views.upload_staff_records, name='upload_staff_records'),
    path('process_bulk_staff_upload/', views.process_bulk_staff_upload, name='process_bulk_staff_upload'),
    path('add_researcher/', views.add_researcher, name='add_researcher'),
    path('login_decide/', views.login_decider, name='login_decider'),

    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('student_logout/', views.student_logout, name='student_logout'),

    # MANAGING USERS
    path('manage_students_users/', views.manage_students, name='manage_students_users'),
    path('manage_staff_users/', views.manage_academic_staff, name='manage_staff_users'),

    path('manage/staff/update/<int:academic_staff_id>/', views.admin_manage_staff_update,
         name='admin_manage_staff_update'),
    path('manage/staff/delete/<int:academic_staff_id>/', views.admin_manage_staff_delete,
         name='admin_manage_staff_delete'),

    #USERS LOGIN
    path('student_login/', views.student_login, name='student_login'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('researcher_login/', views.researcher_login, name='researcher_login'),
    path('content_manager_login/', views.content_manager_login, name='content_manager_login'),

    #USERS PASSWORD UPDATE
    path('student_password_update/', views.students_password_update, name='student_password_update'),

    # USERS DASHBOARD
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    # BOOK CATEGORIES
    path('book_category/', views.book_category, name='book_category'),
    path('get-courses/<str:department>/', views.get_courses, name='get_courses'),

    # UPLOAD BOOKS BY ADMIN
    path('upload_books/', views.upload_materials, name='upload_materials'),

    # upload PDF books
    path('upload_pdf_books/', views.PDF_materials_upload, name='upload_pdf_books'),
    # upload video books
    path('upload_video_books/', views.video_materials_upload, name='upload_video_books'),
    # upload audio books
    path('upload_audio_books/', views.audio_materials_upload, name='upload_audio_books'),
    # upload image books

    # journal materials
    path('upload_journal_books/', views.journal_materials_upload, name='upload_journal_books'),

    # DRIVE BOOKS CATALOGUING

    # DEPT BOOKS CATEGORIES
    path('computer_sci_materials/', views.computer_sci_book_category, name='computer_science_category'),

    # ... other paths ...
    path('view_books/<str:category>/', views.view_books, name='view_books'),

    # COMPUTER SCI DEPT BOOKS
    path('books/<str:category>/', views.view_comp_sci_books, name='view_comp_sci_books'),

    # ... other paths ...
    path('protect_materials', views.view_protected_materials, name='protected_materials'),
    path('protected_cs_cat_materials', views.view_protected_comp_sci_materials, name='protected_comp_category'),
    path('protected_books/<str:category>/', views.view_protected_comp_sci_books, name='view_protected_cs_materials'),
    path('protected_books_details/<str:category>/<path:book_id>/', views.view_protected_book_details, name='view_mat_details'),

    # STAFF SECTION OF THE APP
    path('staff_login/', views.staff_login, name='staff_login'),

    # STAFF pasword update
    path('staff_password_update/', views.staff_update_password, name='staff_password_update'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # RESEARCHER SECTION OF THE APP

    path('researcher_login/', views.researcher_login, name='researcher_login'),
    path('researcher_dashboard/', views.researcher_dashboard, name='researcher_dashboard'),

    #RESEARCH MATERIALS SECTION
    #UPLOAD RESEARCH MATERIALS
    path('upload_research_materials/', views.research_materials_upload, name='upload_research_materials'),
    # RESEARCH REPOSITORY
    path('research_repository/', views.research_repository, name='research_repository'),
    path('research_material_view', views.view_research_materials, name='research_material_view')




]
