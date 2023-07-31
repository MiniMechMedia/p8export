
{{description}}

{% if pico_url %}
Remix it on [pico-8-edu.com]({{pico_url}})
{% endif %}

This cart is tweetable at just {{char_count}} characters.

<pre><code>{{minified_code | htmlSafeSource}}</code></pre>

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
