# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_hidden_block():
    """Test the behavior of generic `block`."""
    prompt = engine("""This is a test {{#block hidden=True}}example{{/block}}""")
    out = prompt()
    assert out.text == "This is a test "


def test_empty_block():
    """Test the behavior of a completely empty `block`."""
    prompt = engine(
        "{{#block}}{{#if nonempty}}{{nonempty}}{{/if}}{{/block}}",
    )
    out = prompt(nonempty=False)
    assert out.text == ""


def test_name_capture():
    prompt = engine(
        "This is a block: {{#block 'my_block'}}text inside block{{/block}}",
    )
    out = prompt()
    assert out["my_block"] == "text inside block"


def test_name_capture_whitespace():
    prompt = engine(
        "This is a block: {{#block 'my_block'}} text inside block {{/block}}",
    )
    out = prompt()
    assert out["my_block"] == " text inside block "
