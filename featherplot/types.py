# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_types.ipynb.

# %% auto 0
__all__ = ['QUADFEATHER_REQUIRED_COLUMNS', 'QUADFEATHER_EXPECTED_COLUMNS', 'Literals', 'Transform', 'Range', 'StringRange',
           'Domain', 'SingleArgumentConditonal', 'TwoArgumentConditional', 'Conditional', 'FunctionalChannel',
           'ConstantChannel', 'BooleanChannel', 'ColorChannel', 'RootChannel', 'TypeGuardError', 'MissingKwargsError',
           'ChannelCreationError', 'LambdaChannelError', 'ConditionalChannelError', 'ConstantChannelError',
           'BasicChannelError', 'CategoricalChannelError', 'LiteralTypeGuard', 'ConditionalTypeGuard',
           'TransformTypeGuard', 'QuadFeatherColumnTypeGuard', 'BaseChannel', 'ConditionalChannel', 'LambdaChannel',
           'ConstantBool', 'ConstantNumber', 'ConstantColor', 'BasicChannel', 'BasicBooleanChannel',
           'CategoricalChannel', 'BasicColorChannel', 'CategoricalColorChannel']

# %% ../nbs/03_types.ipynb 3
from rich.repr import auto as rich_auto
from dataclasses import dataclass, field, asdict
from typing import Optional, Union, Any, List, TypeAlias, Literal, Tuple, get_args, Dict

# %% ../nbs/03_types.ipynb 4
QUADFEATHER_REQUIRED_COLUMNS: TypeAlias = Literal['x', 'y']
QUADFEATHER_EXPECTED_COLUMNS: TypeAlias = Union[QUADFEATHER_REQUIRED_COLUMNS, Literal['z']]

# %% ../nbs/03_types.ipynb 6
from typing import TypeVar

# %% ../nbs/03_types.ipynb 7
Literals = TypeVar('Literals')

@rich_auto
@dataclass
class TypeGuardError(TypeError):
    pass

@rich_auto
@dataclass
class MissingKwargsError(ValueError):
    pass


@rich_auto
@dataclass
class ChannelCreationError(Exception):
    pass

@rich_auto
@dataclass
class LambdaChannelError(ChannelCreationError):
    pass

@rich_auto
@dataclass
class ConditionalChannelError(ChannelCreationError):
    pass

@rich_auto
@dataclass
class ConstantChannelError(ChannelCreationError):
    pass

@rich_auto
@dataclass
class BasicChannelError(ChannelCreationError):
    pass

@rich_auto
@dataclass
class CategoricalChannelError(ChannelCreationError):
    pass


@rich_auto
@dataclass
class LiteralTypeGuard:
    types: Optional[Literals]

    @classmethod
    def check(cls, value: Any) -> bool:
        if cls.types is None: 
            return False
        
        for t in cls.types:
            if value in get_args(t):
                return True
        return False
    @classmethod
    def validate(cls, value: Any) -> None:
        if not cls.check(value):
            raise TypeGuardError(f'{value} not in {cls.types}')
    
@rich_auto
@dataclass
class ConditionalTypeGuard(LiteralTypeGuard):
    types: Optional[Literals] = field(default_factory=lambda : [SingleArgumentConditonal, TwoArgumentConditional])

@rich_auto
@dataclass
class TransformTypeGuard(LiteralTypeGuard):
    types: Optional[Literals] = field(default_factory=lambda : [Transform])

@rich_auto
@dataclass
class QuadFeatherColumnTypeGuard(LiteralTypeGuard):
    types: Optional[Literals] = field(default_factory=lambda : [QUADFEATHER_REQUIRED_COLUMNS, QUADFEATHER_EXPECTED_COLUMNS])


# %% ../nbs/03_types.ipynb 9
Transform: TypeAlias = Literal['literal', 'linaer', 'log', 'sqrt']

Range: TypeAlias = Tuple[Union[int, float], Union[int, float]]
StringRange: TypeAlias = Union[str, List[str]]

Domain: TypeAlias = Tuple[Union[int, float], Union[int, float]]


SingleArgumentConditonal: TypeAlias = Literal['gt', 'lt', 'gte', 'lte', 'eq', 'neq']
TwoArgumentConditional: TypeAlias = Literal['between', 'within']

Conditional: TypeAlias = Union[SingleArgumentConditonal, TwoArgumentConditional]

@rich_auto
@dataclass
class BaseChannel:
    field: str

    def export_tuple_as_list(self, d:Dict[str, Any], key:str) -> Dict[str, Any]:
        val = d.get(key, None)
        if val is not None:
            if type(val) == tuple:
                d[key] = list(val)
        return d
    
    def to_dict(self) -> dict:
        d = asdict(self)

        d = self.export_tuple_as_list(d, 'range')
        d = self.export_tuple_as_list(d, 'domain')
        d = self.export_tuple_as_list(d, 'categories')

        if 'human' in d and d['human'] is None:
            del d['human']
        if 'categories' in d and d['categories'] is None:
            del d['categories']
        return d
    
    def to_meta(self) -> dict:
        d = self.to_dict()
        name = self.__class__.__name__
        d['type'] = name
        return d


@rich_auto
@dataclass
class ConditionalChannel(BaseChannel):
    field: str
    a: Union[int, float]
    b: Optional[Union[int, float]]
    op: Conditional
    human: Optional[str] = None

@rich_auto
@dataclass
class LambdaChannel(BaseChannel):
    field: str
    # NOTE: was called lambda
    lfunc: str
    range: Range
    domain: Domain
    human: Optional[str] = None

FunctionalChannel: TypeAlias = Union[LambdaChannel, ConditionalChannel]

@rich_auto
@dataclass
class ConstantBool(BaseChannel):
    constant: Optional[bool] = 'boolean'
    human: Optional[str] = None

@rich_auto
@dataclass
class ConstantNumber(BaseChannel):
    constant: Optional[Union[int, float]] = 'number'
    human: Optional[str] = None

@rich_auto
@dataclass
class ConstantColor(BaseChannel):
    constant: Optional[str] = 'blue'
    human: Optional[str] = None


ConstantChannel = Union[ConstantBool, ConstantNumber, ConstantColor]

@rich_auto
@dataclass
class BasicChannel(BaseChannel):
    field: str
    transform: Optional[Transform] = 'literal'
    range: Optional[Range] = None
    domain: Optional[Domain] = None
    human: Optional[str] = None

@rich_auto
@dataclass
class BasicBooleanChannel(BasicChannel):
    range: Optional[Range] = (0, 1)
    domain: Optional[Domain] = (0, 1)
    human: Optional[str] = None



@rich_auto
@dataclass
class CategoricalChannel(BaseChannel):
    field: str
    human: Optional[str] = None
   
@rich_auto
@dataclass
class BasicColorChannel(BasicChannel):
    range: Optional[StringRange] = None
    domain: Optional[Domain] = None
    

@rich_auto
@dataclass
class CategoricalColorChannel(CategoricalChannel):
    range: Optional[StringRange] = None
    domain: Optional[List[str]] = None
    # NOTE: not originally in Deepscatter, but added for convenience
    categories: Optional[List[str]] = None


BooleanChannel = Union[ConstantBool, FunctionalChannel, BasicBooleanChannel]
ColorChannel: TypeAlias = Union[BasicColorChannel, CategoricalColorChannel, ConstantColor]
RootChannel: TypeAlias = Union[BooleanChannel, BasicChannel, ConditionalChannel, ConstantChannel, LambdaChannel]
