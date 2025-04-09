from django.test import SimpleTestCase

class BaseTestCase(SimpleTestCase):
    patches = {}

    def setPatches(self, patches):
        self.patches = patches.start()

        for key, value in self.patches.items():
            setattr(self, key, value)

        self.addCleanup(patches.stop)