class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.obj = form.save(commit=False)
            self.obj.user = self.request.user
        return super().form_valid(form)