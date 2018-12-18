from abc import (
    ABC,
)
from typing import (
    Tuple,
    Type,
)

from eth.utils.datatypes import (
    Configurable,
)

from eth.beacon.db.chain import BaseBeaconChainDB
from eth.beacon.types.blocks import BaseBeaconBlock
from eth.beacon.types.states import BeaconState


from .state_transitions import (
    BaseStateTransition,
)
from .configs import (  # noqa: F401
    BeaconConfig,
)


class BaseBeaconStateMachine(Configurable, ABC):
    fork = None  # type: str
    chaindb = None  # type: BaseBeaconChainDB
    config = None  # type: BeaconConfig

    block = None  # type: BaseBeaconBlock
    state = None  # type: BeaconState

    block_class = None  # type: Type[BaseBeaconBlock]
    state_class = None  # type: Type[BeaconState]
    state_transition_class = None  # type: Type[BaseStateTransition]


class BeaconStateMachine(BaseBeaconStateMachine):
    def __init__(self,
                 chaindb: BaseBeaconChainDB,
                 block: BaseBeaconBlock,
                 state: BeaconState) -> None:
        # TODO: get state from DB, now it's just a stub!
        self.state = state

    @classmethod
    def get_block_class(cls) -> Type[BaseBeaconBlock]:
        """
        Return the :class:`~eth.beacon.types.blocks.BeaconBlock` class that this
        StateMachine uses for blocks.
        """
        if cls.block_class is None:
            raise AttributeError("No `block_class` has been set for this StateMachine")
        else:
            return cls.block_class

    @classmethod
    def get_state_class(cls) -> Type[BeaconState]:
        """
        Return the :class:`~eth.beacon.types.states.BeaconState` class that this
        StateMachine uses for BeaconState.
        """
        if cls.state_class is None:
            raise AttributeError("No `state_class` has been set for this StateMachine")
        else:
            return cls.state_class

    @classmethod
    def get_state_transiton_class(cls) -> Type[BaseStateTransition]:
        """
        Return the :class:`~eth.beacon.state_machines.state_transition.state_transition_class`
        class that this StateTransition uses for BeaconState.
        """
        if cls.state_transition_class is None:
            raise AttributeError("No `state_transition_class` has been set for this StateMachine")
        else:
            return cls.state_transition_class

    @property
    def state_transition(self) -> BaseStateTransition:
        return self.get_state_transiton_class()(self.config)

    #
    # Import block API
    #
    def import_block(self, block: BaseBeaconBlock) -> Tuple[BeaconState, BaseBeaconBlock]:
        state = self.state_transition.apply_state_transition(
            self.state,
            block,
        )
        # TODO: Validate state roots
        # TODO: Update self.state
        # TODO: persist states in BeaconChain
        return state, block
