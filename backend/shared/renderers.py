from rest_framework.renderers import JSONRenderer


class EnvelopeRenderer(JSONRenderer):
    """Wraps all responses in the { data, meta, errors } envelope."""

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        status_code = response.status_code if response else 200

        if status_code >= 400:
            envelope = {"data": None, "meta": {}, "errors": data}
        else:
            envelope = {"data": data, "meta": {}, "errors": None}

        return super().render(envelope, accepted_media_type, renderer_context)
