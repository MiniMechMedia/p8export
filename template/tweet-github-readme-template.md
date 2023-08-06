# {{game_name}}
{{description}}

[![{{alt_text}}]({{cover_path}})]({{itch_link}})

{% if pico_url %}
Play it now on [itch.io]({{itch_link}}) or remix it on [pico-8-edu.com]({{pico_url}})
{% else %}
Play it now on [itch.io]({{itch_link}})
{% endif %}

This cart is tweetable at just {{char_count}} characters.

<pre><code>{{minified_code | htmlSafeSource}}</code></pre>

## Explanation
<pre><code>{{clarified_code | htmlSafeSource}}</code></pre>

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
