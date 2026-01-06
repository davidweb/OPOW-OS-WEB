from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re

class SiteNameReplaceMiddleware(MiddlewareMixin):
	"""
	Remplace dans les réponses HTML le texte ancien par le nouveau.
	Par défaut remplace "Noethysweb" par "Opow-Oran".
	Configurer dans settings : SITE_NAME_REPLACEMENT = ("Noethysweb", "Opow-Oran")
	"""
	def __init__(self, get_response=None):
		super().__init__(get_response)
		repl = getattr(settings, "SITE_NAME_REPLACEMENT", ("Noethysweb", "Opow-Oran"))
		if isinstance(repl, (list, tuple)) and len(repl) >= 2:
			self.old = str(repl[0])
			self.new = str(repl[1])
		else:
			self.old = "Noethysweb"
			self.new = "Opow-Oran"
		self.pattern = re.compile(re.escape(self.old))

	def __call__(self, request):
		response = self.get_response(request)
		content_type = response.get("Content-Type", "")
		# Ne toucher qu'aux réponses HTML non streamées
		if "text/html" in content_type and not getattr(response, "streaming", False):
			try:
				# Décoder, remplacer, recoder en respectant le charset de la réponse
				charset = getattr(response, "charset", "utf-8") or "utf-8"
				text = response.content.decode(charset, errors="ignore")
				if self.old in text:
					text = self.pattern.sub(self.new, text)
					response.content = text.encode(charset)
					if response.get("Content-Length"):
						response["Content-Length"] = str(len(response.content))
			except Exception:
				# Ne pas faire échouer la requête en cas d'erreur de manipulation
				pass
		return response
