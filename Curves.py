from numpy import exp


class Curve:
    def __init__(self, lower_bound=0.0, upper_bound=1.0):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.fn = self.get_fn()

    def __call__(self, input):
        if input < self.lower_bound \
                or input > self.upper_bound:
            raise ValueError
        else:
            return self.fn(input)

    def get_fn(self):
        raise NotImplementedError


class Power(Curve):
    def __init__(self,
                 scale: float,
                 power: float,
                 offset: float,
                 lower_bound=0.0,
                 upper_bound=1.0):
        self.scale = scale
        self.power = power
        self.offset = offset
        super().__init__(
            lower_bound=lower_bound,
            upper_bound=upper_bound)

    def get_fn(self):
        return lambda input:\
            (input ** self.power) * self.scale + self.offset


class Linear(Curve):
    def __init__(self,
                 slope: float,
                 y_intercept: float,
                 lower_bound=0.0,
                 upper_bound=1.0):
        self.slope = slope
        self.y_intercept = y_intercept
        super().__init__(
            lower_bound=lower_bound,
            upper_bound=upper_bound)

    def get_fn(self):
        return lambda input:\
            input * self.slope + self.y_intercept


class NegativeSigmoid(Curve):
    def __init__(self,
                 spread: float,
                 center: float,
                 lower_bound=0.0,
                 upper_bound=1.0):
        self.center = center
        self.spread = spread
        super().__init__(
            lower_bound=lower_bound,
            upper_bound=upper_bound)

    def get_fn(self):
        # TODO remove hardcode
        return lambda input:\
            1 / (1 + exp(input))


def create_curve(curve_config: dict):
    curve_type = curve_config['type']
    del curve_config['type']
    CurveClass = None
    if curve_type == 'linear':
        CurveClass = Linear
    elif curve_type == 'power':
        CurveClass = Power
    elif curve_type == 'negative-sigmoid':
        CurveClass = NegativeSigmoid
    else:
        print("[Curves] Unsupported curve type:",
              curve_type)
        exit()
    return CurveClass(**curve_config)
