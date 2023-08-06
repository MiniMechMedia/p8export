
{{description}}

{% if pico_url %}
Remix it on [pico-8-edu.com]({{pico_url}})
{% endif %}

This cart is tweetable at just {{char_count}} characters.

```lua
{{minified_code | htmlSafeSource}}
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

See the explainer on [GitHub]({{code_explainer_link}})

{% if acknowledgements %}
## Acknowledgements
{{acknowledgements}}
{% endif %}
