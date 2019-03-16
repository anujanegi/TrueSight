from modules.text_detection.text_detection import TextDetector


def create_knowledge_graph(frame):
    """
    format:
    {
        classes:{
            class1: {
                count: n1
                objects: {
                    class1object1: {
                        distance: distance_from_camera
                    },
                    class1object2: {
                        distance: distance_from_camera
                    },
                    ...
                }
            },
            ...
        },
        mode: current_scenery_mode (eg. traffic, indoor, park)
        text: ? (optional)
    }
    :param frame: input image
    :return: knowledge graph
    """
    knowledge = {}
    text = TextDetector.detect(frame)
    if text:
        knowledge["text"] = text
    return knowledge



