from .authenticated_controller import AuthenticatedController


class AuthenticatedFarmVegetableController(AuthenticatedController):
    def fix_data(self):
        self.data["farmer"] = self.user.id
        self.data["created_by"] = str(self.user.email)
        self.data["updated_by"] = str(self.user.email)
        self.data["farm"] = self.user.farm.id
