{
    "name": "G2P Self Service Portal",
    "category": "G2P",
    "version": "17.0.0.0.0",
    "sequence": 1,
    "author": "OpenG2P",
    "website": "https://openg2p.org",
    "license": "LGPL-3",
    "depends": [
        "g2p_registry_base",
        "g2p_registry_individual",
        "g2p_programs",
        "g2p_program_registrant_info",
        "g2p_program_documents",
        "website",
        "web",
        "g2p_portal_auth",
    ],
    "data": [
        "data/g2p_self_service_form_action_data.xml",
        "views/g2p_self_service_authentication.xml",
        "views/g2p_self_service_base.xml",
        "views/g2p_self_service_login.xml",
        "views/g2p_self_service_dashboard.xml",
        "views/g2p_self_service_allprograms.xml",
        "views/g2p_self_service_help.xml",
        "views/g2p_self_service_myprofile.xml",
        "views/g2p_self_service_aboutus.xml",
        "views/g2p_self_service_otherpage.xml",
        "views/g2p_self_service_contactus.xml",
        "views/g2p_self_service_form_page_template.xml",
        "views/program_view.xml",
        "views/g2p_self_service_signup.xml",
        "views/g2p_self_service_submission_info.xml",
        "views/g2p_self_service_submitted_forms.xml",
        "views/res_config_settings.xml",
        "views/website_page.xml",
        "wizard/g2p_self_service_program_view_wizard.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "g2p_self_service_portal/static/src/js/self_service_form_action.js",
            # # "g2p_self_service_portal/static/src/js/self_service_pie_chart.js",
            # "g2p_self_service_portal/static/src/js/self_service_search_sort.js",
            # "g2p_self_service_portal/static/src/js/self_service_search_sort_all.js",
            # "g2p_self_service_portal/static/src/js/self_service_welcome_alert.js"
        ],
        "website.assets_wysiwyg": [
            "g2p_self_service_portal/static/src/js/apply_program_form_editor.js",
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
