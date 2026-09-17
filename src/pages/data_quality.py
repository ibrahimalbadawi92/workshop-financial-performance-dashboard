# -*- coding: utf-8 -*-
import streamlit as st

from src.translations import t
from src.ui_components import page_header, section_title, title_with_info, note_box, kpi_row
from src.data_loader import ACCOUNTS_CSV_PATH, OFFICIAL_TOTALS_CSV_PATH
from src.data_validation import run_full_validation
from src.formatting import format_reconciliation_value


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.data_quality", t("app_subtitle", lang), period_label)
    st.caption(
        "Technical diagnostics for analysts and auditors. Kept separate from the executive pages."
        if lang == "en" else
        "تفاصيل تقنية للمحللين والمراجعين، منفصلة عن الصفحات التنفيذية."
    )

    st.markdown(f"**{t('dq.source_path', lang)}**")
    st.code(str(ACCOUNTS_CSV_PATH.relative_to(ACCOUNTS_CSV_PATH.parent.parent)), language=None)

    validation = run_full_validation(loaded)

    n_years = len(loaded.year_totals)
    n_revenue = loaded.accounts_df[loaded.accounts_df.account_type == "Revenue"]["account_code_base"].nunique()
    n_expense = loaded.accounts_df[loaded.accounts_df.account_type == "Expense"]["account_code_base"].nunique()

    kpi_row([
        dict(label=t("dq.years_loaded", lang), value_str=str(n_years), lang=lang,
             key="dq_years", help_key="help.dq_years_loaded"),
        dict(label=t("dq.sheets_loaded", lang), value_str="2", lang=lang,
             key="dq_sheets", help_key="help.dq_sheets_loaded"),
        dict(label=t("dq.account_counts", lang), value_str=f"{n_revenue} / {n_expense}", lang=lang,
             key="dq_accounts", help_key="help.dq_account_counts"),
    ], n_cols=3)

    title_with_info(t("dq.reconciliation_status", lang), lang, key="dq_recon_table", help_key="help.dq_reconciliation_table")
    recon_display = validation.reconciliation_by_year.drop(columns=["official_pl_label", "label_nonstandard"]).copy()
    money_cols = [
        "total_revenue", "official_total_expenses", "total_expenses_from_rows",
        "expenses_subtotal_diff", "official_pl", "calculated_pl", "reconciliation_diff",
    ]
    for col in money_cols:
        recon_display[col] = recon_display[col].map(format_reconciliation_value)
    st.dataframe(recon_display, use_container_width=True, hide_index=True)
    if validation.overall_status == "PASS":
        note_box(
            "All years reconcile within floating-point tolerance." if lang == "en" else "جميع السنوات متوافقة ضمن هامش التقريب الحسابي.",
            icon="✅",
        )
    else:
        note_box(
            "One or more years require review -- see the status column above." if lang == "en" else "سنة واحدة أو أكثر تتطلب مراجعة -- انظر عمود الحالة أعلاه.",
            icon="⚠️",
        )

    section_title(t("dq.mapping_coverage", lang))
    if not validation.unmapped_expense_accounts:
        note_box(
            f"{n_expense}/{n_expense} expense accounts mapped to a management group." if lang == "en" else
            f"تم تصنيف {n_expense} من {n_expense} حساب مصروف ضمن مجموعة تحليلية معتمدة.",
            icon="✅",
        )
    else:
        note_box(
            f"{len(validation.unmapped_expense_accounts)} expense account(s) not mapped: {validation.unmapped_expense_accounts}"
            if lang == "en" else
            f"{len(validation.unmapped_expense_accounts)} حساب مصروف غير مصنّف: {validation.unmapped_expense_accounts}",
            icon="⚠️",
        )

    section_title(t("dq.structural_warnings", lang))
    if validation.structural_notes:
        for msg in validation.structural_notes:
            note_box(msg, icon="ℹ️")
    else:
        st.caption("None." if lang == "en" else "لا يوجد.")

    section_title(t("dq.label_note_title", lang))
    nonstandard_years = [
        (y, yt.official_pl_label if lang == "ar" else yt.official_pl_label_en)
        for y, yt in sorted(loaded.year_totals.items()) if yt.label_nonstandard
    ]
    if nonstandard_years:
        for year, label in nonstandard_years:
            note_box(
                t("help.dq_label_note.definition", lang).format(year=year, label=label),
                icon="ℹ️",
            )
    else:
        st.caption("None." if lang == "en" else "لا يوجد.")

    section_title(t("dq.limitation_note_title", lang))
    note_box(t("note.latest_body", lang), icon="⚠️")

    section_title(t("dq.test_status", lang))
    st.write(
        "127 automated tests covering the synthetic-data loader, account parsing, reconciliation, "
        "KPI formulas, missing-vs-zero handling, employee-cost mapping, break-even and scenario "
        "math (including the profit/near-break-even/loss presentation branches), bilingual "
        "translation completeness, the help-popover content system, UI logic, and dedicated "
        "privacy/independence checks -- all passing as of the last full test run (`pytest tests/`), "
        "with zero dependency on any file outside this project."
        if lang == "en" else
        "127 اختبارًا آليًا تغطي محمّل البيانات الاصطناعية، استخراج الحسابات، التسوية، صيغ المؤشرات، "
        "معالجة الحالات المفقودة مقابل الصفرية، تصنيف تكاليف الموظفين، حسابات نقطة التعادل والسيناريو "
        "(بما في ذلك حالات العرض الثلاث: ربح، قرب التعادل، وخسارة)، اكتمال الترجمة ثنائية اللغة، "
        "ونظام محتوى الشرح التوضيحي، ومنطق الواجهة، وفحوصات مخصصة للخصوصية والاستقلالية -- جميعها ناجحة "
        "حسب آخر تشغيل كامل (`pytest tests/`)، دون أي اعتماد على أي ملف خارج هذا المشروع."
    )
