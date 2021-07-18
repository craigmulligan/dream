from sqlalchemy import event


class TransactionManager:
    # Thanks
    # http://paulbecotte.com/entry/how-to-wrap-flask-sqlalchemy-unit-tests-in-a-database-transaction
    def __init__(self, db, app):
        self.db = db
        self.app = app

    def _start_transaction(self):
        # Create a db session outside of the ORM that we can roll back
        self.connection = self.db.engine.connect()
        self.trans = self.connection.begin()

        # bind db.session to that connection, and start a nested transaction
        self.db.session = self.db.create_scoped_session(
            options={"bind": self.connection}
        )
        self.db.session.begin_nested()

        # sets a listener on db.session so that whenever the transaction ends-
        # commit() or rollback() - it restarts the nested transaction
        @event.listens_for(self.db.session, "after_transaction_end")
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.begin_nested()

        self._after_transaction_end_listener = restart_savepoint

    def _close_transaction(self):
        # Remove listener
        event.remove(
            self.db.session,
            "after_transaction_end",
            self._after_transaction_end_listener,
        )
        # Roll back the open transaction and return the db connection to
        # the pool
        self.db.session.close()
        self.db.get_engine(self.app).dispose()
        self.trans.rollback()

        # Reset all db seq to 0 this is so that snapshots and other static
        # seq id matches work.
        seqs = self.connection.execute(
            """
            SELECT c.relname as name FROM pg_class c WHERE c.relkind = 'S';
        """
        )

        for seq in seqs:
            self.connection.execute(
                """
                ALTER SEQUENCE {} RESTART;
            """.format(
                    seq.name
                )
            )

        self.connection.invalidate()
