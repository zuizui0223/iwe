from scripts.screen_hurlburt2004_thesis_text import rank_pages, score_page, short_context


def test_page_triage_is_heuristic_only_and_preserves_physical_pdf_locator():
    a = "Overview of Yucca species and geography " * 15
    b = ("Marked clone and inflorescence observations on several dates, "
         "followed by fruit dissections and viable seed counts. ") * 8
    out = rank_pages([a, b], max_pages=5)
    assert out[0]["physical_pdf_page"] == 2
    assert out[0]["join_verified"] is False
    assert out[0]["score"] > 10


def test_text_screen_does_not_infer_source_id_join_from_keywords():
    x = "Marked flowers examined and fruits elsewhere sampled for seeds."
    score, groups = score_page(x)
    assert score > 0 and "marked_units" in groups
    assert isinstance(short_context(x), str)
    assert len(short_context(x)) <= 220
