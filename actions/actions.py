import weakref
import logging

from obj.entity import EntityClass, EntityState

# Abstract action:
class AbstractAction:

    def __init__(self): self._is_obsolete = False

    def is_obsolete(self): return self._is_obsolete

    def set_obsolete(self): self._is_obsolete = True

    def set_relevant(self): self._is_obsolete = False

    def execute(self)   : raise NotImplementedError()

    def undo(self)      : raise NotImplementedError()

    def redo(self)      : raise NotImplementedError()

    def cleanup(self)   : raise NotImplementedError()

# Class BatchActions: Groups actions together and executes them
class BatchActions(AbstractAction):

    # Initializer:
    def __init__(self, actions: list | None):

        # Initialize base-class:
        super().__init__()

        # Actions-sequence:
        self.actions = actions or []

    # Return batch-size:
    def size(self): return len(self.actions)

    # Re-implement `set_obsolete`:
    def set_obsolete(self):

        # Call `set_obsolete` for each action:
        for action in self.actions:
            action.set_obsolete()

    # Add actions to the batch:
    def add_to_batch(self, actions: AbstractAction | list)    -> None :

        if   isinstance(actions, list):             self.actions += actions
        elif isinstance(actions, AbstractAction):   self.actions.append(actions)

    # Cleanup when stack is pruned:
    def cleanup(self)   -> None :
        for action in self.actions:
            action.cleanup()

    # Execute batch-actions:
    def execute(self)   -> None :
        for action in self.actions:
            action.execute()

    # Undo batch-operations:
    def undo(self)  -> None :
        for action in reversed(self.actions):
            action.undo()

    # Redo batch-operations:
    def redo(self)  -> None :
        for action in reversed(self.actions):
            action.redo()

# Class CreateVertexAction: For vertex operations (create, undo/redo)
class CreateVertexAction(AbstractAction):

    # Initializer:
    def __init__(self, canvas, vertex):

        # Initialize base-class:
        super().__init__()

        # References:
        self.cref = weakref.ref(canvas)
        self.vref = weakref.ref(vertex)

        # Connect objects' destroyed signals:
        self.cref().destroyed.connect(self.set_obsolete)
        self.vref().destroyed.connect(self.set_obsolete)

    # Triggered by stack-manager's prune functions:
    def cleanup(self):

        # If obsolete, log and return:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, aborting cleanup!")
            return

        cref = self.cref()  # Dereference canvas pointer
        vref = self.vref()  # Dereference vertex pointer

        # If vertex exists in canvas' database and is not active, remove it:
        if (
            vref in cref.db.vertex.keys() and
            not cref.db.vertex[vref]
        ):
            cref.db.vertex.pop(vref, None)    # Remove vertex from canvas' database
            vref.deleteLater()              # Delete vertex

    # Execute action:
    def execute(self): pass

    # Undo operation:
    def undo(self):

        # Abort-conditions:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute undo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        vref = self.vref()  # Dereference vertex pointer

        # Deactivate vertex:
        cref.db.vertex[vref] = EntityState.HIDDEN         # Hide the vertex
        vref.setVisible(False)                          # Toggle-off visibility
        vref.blockSignals(True)                         # Block signals

    # Redo operation:
    def redo(self)  -> None:

        # Abort-conditions:
        if self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute redo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        vref = self.vref()  # Dereference vertex pointer

        # Re-activate vertex:
        cref.db.vertex[vref] = EntityState.ACTIVE       # Mark vertex as reactivated (i.e. False) in the canvas' database
        vref.blockSignals(False)        # Toggle-on visibility
        vref.setVisible(True)           # Unblock signals

# Class RemoveVertexAction: For vertex operations (delete, undo/redo)
class RemoveVertexAction(AbstractAction):

    # Initializer:
    def __init__(self, canvas, vertex):

        # Initialize base-class:
        super().__init__()

        # Strong reference(s):
        self.cref = weakref.ref(canvas)
        self.vref = weakref.ref(vertex)

        # Connect objects' destroyed signal:
        self.cref().destroyed.connect(self.set_obsolete)
        self.vref().destroyed.connect(self.set_obsolete)

    # Cleanup when the stack is pruned:
    def cleanup(self)   -> None :

        # Abort-conditions:
        if  self._is_obsolete:
            logging.info(f"References destroyed, this action is obsolete")
            return

        cref = self.cref()  # Dereference canvas pointer
        vref = self.vref()  # Dereference vertex pointer

        # If vertex exists in canvas' database and is not active, remove it:
        if (
            vref in cref.db.vertex.keys() and
            not cref.db.vertex[vref]
        ):

            # Delete the vertex's handles (and connections):
            for _eclass in [EntityClass.INP, EntityClass.OUT]:
                while vref[_eclass]:
                    handle, state = vref[_eclass].popitem()
                    if (
                        handle.connected and
                        handle.connector()
                    ):
                        handle.connector().deleteLater()

            # Remove vertex from canvas, then delete it:
            cref.db.vertex.pop(vref, None)
            vref.deleteLater()

    # Execute action:
    def execute(self)   -> None :

        # Abort-conditions:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute do-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        vref = self.vref()  # Dereference vertex pointer

        # Note: The for-loop below removes connectors from the canvas' database. This is necessary to ensure 
        #       that the symbols for new connections are contiguous.

        for handle in vref[EntityClass.INP] | vref[EntityClass.OUT]:

            # For all connected handles
            if (
                handle.connected and 
                handle.connector()
            ):
                handle.conjugate().free()                   # Free the handle's conjugate
                handle.connector().setVisible(False)        # Toggle-off connector's visibility
                cref.db.vector[handle.connector()] = EntityState.HIDDEN    # Mark connector as deactivated in the canvas' database

        # Deactivate vertex:
        cref.db.vertex[vref] = EntityState.HIDDEN      # Mark vertex as deactivated in the canvas' database
        vref.setVisible(False)          # Toggle-off visibility
        vref.blockSignals(True)         # Block signals

    # Undo operation:
    def undo(self)  -> None :

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute undo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        vref = self.vref()  # Dereference vertex pointer

        # Add connectors back to the canvas' database:
        for handle in vref[EntityClass.INP] | vref[EntityClass.OUT]:

            # For all connected handles:
            if (
                handle.connected and 
                handle.connector()
            ):
                handle.conjugate().lock(handle, handle.connector()) # Lock the handle's conjugate
                handle.connector().setVisible(True)                 # Toggle-on connector's visibility  
                cref.db.vector[handle.connector()] = EntityState.ACTIVE             # Mark the connector as reactivated in the canvas' database

        # Reactivate vertex:
        cref.db.vertex[vref] = EntityState.ACTIVE
        vref.blockSignals(False)
        vref.setVisible(True)

    # Redo operation:
    def redo(self)  -> None:    self.execute()

# Class CreateStreamAction: For stream operations (create, undo/redo)
class CreateStreamAction(AbstractAction):

    # Initializer:
    def __init__(self, canvas, terminal):

        # Initialize base-class:
        super().__init__()

        # References:
        self.cref = weakref.ref(canvas)
        self.tref = weakref.ref(terminal)

        # Connect objects' destroyed signals:
        self.cref().destroyed.connect(self.set_obsolete)
        self.tref().destroyed.connect(self.set_obsolete)

    # Triggered by stack-manager's prune functions:
    def cleanup(self):

        # If obsolete, log and return:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, this action is obsolete")
            return

        cref = self.cref()
        tref = self.tref()

        # If terminal exists in canvas' database and is not active, remove it:
        if (
            tref in cref.db.stream.keys() and
            not cref.db.stream[tref]
        ):
            cref.db.stream.pop(tref, None)    # Remove terminal from canvas' database
            tref.deleteLater()              # Delete terminal

    # Execute action:
    def execute(self): pass

    # Undo operation:
    def undo(self):

        # Abort-condition:
        if self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute undo-action")
            return
        
        cref = self.cref()  # Dereference canvas pointer
        tref = self.tref()  # Dereference terminal pointer

        # If terminal is connected, disconnect:
        if (
            tref.handle.connected and
            tref.handle.conjugate() and 
            tref.handle.connector()
        ):
            tref.handle.conjugate().free()
            tref.handle.connector().setVisible(False)
            tref.handle.connector().blockSignals(True)

        # Deactivate terminal:
        cref.db.stream[tref] = EntityState.HIDDEN
        tref.setVisible(False)
        tref.blockSignals(True)

    # Redo operation:
    def redo(self)  -> None:

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute redo-action")
            return
        
        cref = self.cref()  # Dereference canvas pointer
        tref = self.tref()  # Dereference terminal pointer

        # If terminal is connected, disconnect:
        if (
            tref.handle.connected and
            tref.handle.conjugate() and 
            tref.handle.connector()
        ):
            tref.handle.conjugate().lock(tref.handle, tref.handle.connector())
            tref.handle.connector().blockSignals(False)
            tref.handle.connector().setVisible(True)

        # Reactivate terminal:
        cref.db.stream[tref] = EntityState.ACTIVE
        tref.blockSignals(False)
        tref.setVisible(True)

# Class RemoveStreamAction: For stream operations (delete, undo/redo)
class RemoveStreamAction(AbstractAction):

    # Initializer:
    def __init__(self, canvas, terminal):

        # Initialize base-class:
        super().__init__()

        # Strong reference(s):
        self.cref = weakref.ref(canvas)
        self.tref = weakref.ref(terminal)

        # Connect objects' destroyed signal:
        self.cref().destroyed.connect(self.set_obsolete)
        self.tref().destroyed.connect(self.set_obsolete)

    # Cleanup when the stack is pruned:
    def cleanup(self)   -> None :

        # Null-check:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, this action is obsolete")
            return

        cref = self.cref()  # Dereference canvas pointer
        tref = self.tref()  # Dereference terminal pointer

        # If terminal exists in canvas' database and is not active, remove it:
        if (
            tref in cref.db.stream.keys() and
            not cref.db.stream[tref]
        ):
            cref.db.stream.pop(tref, None)    # Remove terminal from canvas' database
            tref.deleteLater()              # Delete terminal

    # Execute action:
    def execute(self)   -> None :

        # Null-check:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute do-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        tref = self.tref()  # Dereference terminal pointer

        # If terminal is connected, disconnect:
        if (
            tref.handle.connected and
            tref.handle.conjugate() and 
            tref.handle.connector()
        ):
            tref.handle.conjugate().free()
            tref.handle.connector().setVisible(False)
            tref.handle.connector().blockSignals(True)

        # Deactivate terminal:
        cref.db.stream[tref] = EntityState.HIDDEN
        tref.setVisible(False)
        tref.blockSignals(True)

    # Undo operation:
    def undo(self)  -> None :

        # Null-check:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute undo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        tref = self.tref()  # Dereference terminal pointer

        # Reconnect terminal with its conjugate:
        if (
            tref.handle.connected and
            tref.handle.conjugate() and 
            tref.handle.connector()
        ):
            tref.handle.conjugate().lock(tref.handle, tref.handle.connector())
            tref.handle.connector().blockSignals(False)
            tref.handle.connector().setVisible(True)

        # Reactivate terminal:
        cref.db.stream[tref] = EntityState.ACTIVE
        tref.blockSignals(False)
        tref.setVisible(True)

    # Redo operation:
    def redo(self):

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute redo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        tref = self.tref()  # Dereference terminal pointer

        # Reconnect terminal with its conjugate:
        if (
            tref.handle.connected and
            tref.handle.conjugate() and 
            tref.handle.connector()
        ):
            tref.handle.conjugate().free()
            tref.handle.connector().setVisible(False)
            tref.handle.connector().blockSignals(True)

        # Deactivate terminal:
        cref.db.stream[tref] = EntityState.HIDDEN
        tref.setVisible(False)
        tref.blockSignals(True)

# Class CreateHandleAction: For handle operations (create, undo/redo)
class CreateHandleAction(AbstractAction):

    # Initializer:
    def __init__(self, vertex, handle):

        # Initialize base-class:
        super().__init__()

        # Weak reference(s):
        self.vref = weakref.ref(vertex)
        self.href = weakref.ref(handle)

        # Connect objects' destroyed signal:
        self.vref().destroyed.connect(self.set_obsolete)
        self.href().destroyed.connect(self.set_obsolete)

    # Cleanup operation
    def cleanup(self)   -> None :

        # Null-check:
        if self._is_obsolete:
            logging.info(f"Reference(s) destroyed, this action is obsolete")
            return

        vref = self.vref()  # Dereference vertex pointer
        href = self.href()  # Dereference handle pointer

        # If handle exists in vertex's database, remove it:
        if (
            href in vref[href.eclass].keys() and
            vref[href.eclass][href] == EntityState.HIDDEN
        ):
            vref[href.eclass].pop(href, None)   # Remove handle from vertex's database
            href.deleteLater()

    # Execute operation:
    def execute(self): pass

    # Undo operation:
    def undo(self)  -> None:

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"References destroyed, cannot execute undo-action")
            return

        vref = self.vref()  # Dereference vertex pointer
        href = self.href()  # Dereference handle pointer

        # Deactivate handle:
        href.setVisible(False)
        href.blockSignals(True)
        vref[href.eclass][href] = EntityState.HIDDEN

    # Redo operation:
    def redo(self)  -> None:

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute redo-action")
            return

        vref = self.vref()  # Dereference vertex pointer
        href = self.href()  # Dereference handle pointer

        # Reactivate handle:
        href.blockSignals(False)
        href.setVisible(True)
        vref[href.eclass][href] = EntityState.ACTIVE

# Class RemoveHandleAction: For handle operations (delete, undo/redo)
class RemoveHandleAction(AbstractAction):

    # Initializer:
    def __init__(self, vertex, handle):

        # Initialize base-class:
        super().__init__()

        # Strong reference(s):
        self.vref = weakref.ref(vertex)
        self.href = weakref.ref(handle)

        # Connect objects' destroyed signal:
        self.vref().destroyed.connect(self.set_obsolete)
        self.href().destroyed.connect(self.set_obsolete)

    # Cleanup operation:
    def cleanup(self)   -> None:

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, this action is obsolete")
            return

        vref = self.vref()  # Dereference vertex pointer
        href = self.href()  # Dereference handle pointer

        # If the handle exists in the vertex's database, remove it:
        if (
            href in vref[href.eclass].keys() and
            vref[href.eclass][href] != EntityState.ACTIVE
        ):
            vref[href.eclass].pop(href, None)   # Remove handle from vertex's database
            href.free(delete_connector = True)  # Delete handle's connector
            href.deleteLater()                  # Delete handle

    # Execute operation:å
    def execute(self):

        # Abort-conditions:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute do-action")
            return

        vref = self.vref()  # Dereference vertex pointer
        href = self.href()  # Dereference handle pointer
        cref = href.scene()

        # Free the handle's conjugate
        if (
            href.conjugate and
            href.connector
        ):
            href.conjugate().free()
            href.connector().setVisible(False)
            cref.db.vector[href.connector()] = EntityState.HIDDEN                        # Mark the connector as deactivated in the canvas' database

        # Deactivate handle:
        href.setVisible(False)
        href.blockSignals(True)

        # Deactivate handle:
        vref[href.eclass][href] = EntityState.HIDDEN

    # Undo operation:
    def undo(self)  -> None:

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute undo-action")
            return

        vref = self.vref()
        href = self.href()
        cref = href.scene()

        # Reconnect handle with its conjugate:
        if (
            href.conjugate and
            href.connector
        ):
            href.conjugate().lock(href, href.connector())
            href.connector().blockSignals(False)
            href.connector().setVisible(True)
            cref.db.vector[href.connector()] = EntityState.ACTIVE         # Mark the connector as reactivated in the canvas' database

        href.blockSignals(False)
        href.setVisible(True)
        vref[href.eclass][href] = EntityState.ACTIVE

    # Redo operation:
    def redo(self)  -> None:

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute redo-action")
            return

        vref = self.vref()
        href = self.href()

        # Remove the handle's connector:
        if (
            href.conjugate and
            href.connector
        ):
            href.conjugate().free()
            href.connector().setVisible(False)
            href.connector().blockSignals(True)

        # Deactivate handle:
        href.setVisible(False)
        href.blockSignals(True)
        vref[href.eclass][href] = EntityState.HIDDEN

# Class ConnectHandleAction: For connector operations (create, undo/redo)
class CreateVectorAction(AbstractAction):

    def __init__(self, canvas, connector):

        # Initialize base-class:
        super().__init__()

        # Strong reference(s):
        self.cref = weakref.ref(canvas)
        self.lref = weakref.ref(connector)

        # Connect objects' destroyed signals:
        self.cref().destroyed.connect(self.set_obsolete)
        self.lref().destroyed.connect(self.set_obsolete)

    def cleanup(self) -> None:

        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, this action is obsolete")
            return

        cref = self.cref()  # Dereference canvas pointer
        lref = self.lref()  # Dereference connector pointer

        # If the connector exists in canvas' database and is not active, remove it:
        if (
            lref in cref.db.vector.keys() and
            not cref.db.vector[lref]
        ):
            cref.db.vector.pop(lref, None)    # Remove connector from canvas' database
            lref.deleteLater()              # Delete connector

    def execute(self):  pass

    def undo(self):

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute undo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        lref = self.lref()  # Dereference connector pointer

        # Free handles:
        lref.origin.free()
        lref.target.free()

        # Deactivate connector:
        lref.setVisible(False)
        lref.blockSignals(True)
        cref.db.vector[lref] = False

    def redo(self):

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute redo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        lref = self.lref()  # Dereference connector pointer

        # Pair handles:
        lref.origin.pair(lref, lref.target)
        lref.target.pair(lref, lref.origin)

        # Deactivate connector:
        lref.setVisible(True)
        lref.blockSignals(False)
        cref.db.vector[lref] = EntityState.ACTIVE

# Class DisconnectHandleAction: For connector operations (delete, undo/redo)
class DeleteVectorAction(AbstractAction):

    def __init__(self, canvas, connector):

        # Initialize base-class:
        super().__init__()

        # Strong reference(s):
        self.cref = weakref.ref(canvas)
        self.lref = weakref.ref(connector)

        # Connect objects' destroyed signal:
        self.cref().destroyed.connect(self.set_obsolete)
        self.lref().destroyed.connect(self.set_obsolete)

    def cleanup(self):

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, this action is obsolete")
            return

        cref = self.cref()  # Dereference canvas pointer
        lref = self.lref()  # Dereference connector pointer

        # If connector exists in canvas' database and is not active, remove it:
        if (
            lref in cref.db.vector.keys() and
            not cref.db.vector[lref]
        ):
            cref.db.vector.pop(lref, None)    # Remove connector from canvas' database
            lref.deleteLater()              # Delete connector

    def execute(self):

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute do-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        lref = self.lref()  # Dereference connector pointer

        # Free handles:
        lref.origin.free()
        lref.target.free()

        # Deactivate connector:
        cref.db.vector.pop(lref, None)
        lref.setVisible(False)
        lref.blockSignals(True)

    def undo(self) -> None:

        # Abort-condition:
        if  self._is_obsolete:
            logging.info(f"Reference(s) destroyed, cannot execute undo-action")
            return

        cref = self.cref()  # Dereference canvas pointer
        lref = self.lref()  # Dereference connector pointer

        # Pair handles:
        lref.origin.pair(lref, lref.target)
        lref.target.pair(lref, lref.origin)

        # Reactivate connector:
        lref.setVisible(True)
        lref.blockSignals(False)
        cref.db.vector[lref] = EntityState.ACTIVE

    def redo(self): self.execute()