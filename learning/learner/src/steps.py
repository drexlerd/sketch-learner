import copy


class Step:
    def __init__(self, **kwargs):
        self.config = self.process_config(self.parse_config(**kwargs))

    def process_config(self, config):
        return config  # By default, we do nothing

    def get_required_attributes(self):
        raise NotImplementedError()

    def get_required_data(self):
        raise NotImplementedError()

    def parse_config(self, **kwargs):
        config = copy.deepcopy(kwargs)
        for attribute in self.get_required_attributes():
            if attribute not in kwargs:
                raise RuntimeError(f'Missing configuration parameter "{attribute}" in pipeline step "{self.__class__}"')
            config[attribute] = kwargs[attribute]
        return config

    def description(self):
        raise NotImplementedError()

    def get_step_runner(self):
        raise NotImplementedError()


class GenerateStateSpacesStep(Step):
    """ Generates state spaces from PDDL files. """
    def process_config(self, config):
        return config

    def get_required_attributes(self):
        return []

    def get_required_data(self):
        return []

    def description(self):
        return "Generate state spaces module"

    def get_step_runner(self):
        """Implement what is to be done
        """
        from . import step_generate_state_spaces
        return step_generate_state_spaces.run


class LearningSketchesStep(Step):
    """ Incrementally learns a sketch by considering more and more instances """
    def process_config(self, config):
        return config

    def get_required_attributes(self):
        return []

    def get_required_data(self):
        return ["generate_state_space"]

    def description(self):
        return "Incremental learning module"

    def get_step_runner(self):
        """Implement what is to be done
        """
        from . import step_learning_sketches
        return step_learning_sketches.run


def generate_pipeline(pipeline, **kwargs):
    pipeline = DEFAULT_PIPELINES[pipeline] if isinstance(pipeline, str) else pipeline
    pipeline, config = generate_pipeline_from_list(pipeline, **kwargs)
    return pipeline, config


def generate_pipeline_from_list(elements, **kwargs):
    steps = []
    config = kwargs
    for klass in elements:
        step = klass(**config)
        config = step.config
        steps.append(step)
    return steps, config


DEFAULT_PIPELINES = dict(
    sketch=[
        GenerateStateSpacesStep,
        LearningSketchesStep
    ],
)
