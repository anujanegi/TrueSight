import inflect

class SentenceFormation:
    def __init__(self):
        self.ie = inflect.engine()

    def scene_sentence(self, scene):
        """
        describe scene
        Example:
            You are in a classroom.
        :param scene: scene of the frame
        :return: sentence descibing scene
        """
        return "You are in %s" % (
            self.ie.a(scene)
        )

    def known_face_sentence(self, known_face_name):
        """
        describe known person
        Example:
            Anuja is in front of you.
        :param known_face_name: name of known person in the frame
        :return: sentence descibing person
        """
        return "%s in front of you" % (
            known_face_name
        )

    def object_sentence(self, object):
        """
        inform object presence
        Example:
            There is a chair.
        :param object: object name
        :return: sentence informing object presence
        """
        return "There is %s" % (
            self.ie.a(object)
        )
