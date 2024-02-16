# {{game_name}}
{{description}}

[![{{alt_text}}]({{cover_path}})]({{itch_link}})

Leave a comment on [itch.io]({{itch_link}})

This cart is tweetable at just {{char_count}} characters.

## Source
Remix it on [pico-8-edu.com]({{pico_url_minified}})
```lua
{{minified_code | htmlSafeSource}}
```

## Explanation
Remix it on [pico-8-edu.com]({{pico_url_clarified}})
```lua
{{clarified_code | htmlSafeSource}}
```

{% if controls %}
## Controls
{{controls}}
{% endif %}

{% if hints %}
## Hints
{{hints}}
{% endif %}

## About
{{jam_info}}

{{about_extra}}

Source code available on [GitHub]({{source_code_link}})

{% if acknowledgements %}
## Acknowledgements
{{acknowledgements}}
{% endif %}
