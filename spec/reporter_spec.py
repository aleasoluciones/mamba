from expects import expect
from doublex import *

from spec.object_mother import *

from mamba import reporter, formatters, example, example_group


with description(reporter.Reporter) :

    with before('each'):
        self.example = an_example()
        self.formatter = Spy(formatters.Formatter)
        self.reporter = reporter.Reporter(self.formatter)
        self.reporter.start()

    with context('when event started'):
        with before('each'):
            self.reporter.example_started(self.example)

        with it('notifies event example started to listeners'):
            assert_that(self.formatter.example_started, called().with_args(self.example))

        with it('increases example counter'):
            expect(self.reporter.example_count).to.be.equal(1)

    with context('when event passed'):
        with it('notifies event example passed to listeners'):
            self.reporter.example_passed(self.example)

            assert_that(self.formatter.example_passed, called().with_args(self.example))

    with context('when event failed'):
        with before('each'):
            self.reporter.example_failed(self.example)

        with it('notifies event example failed to listeners'):
            assert_that(self.formatter.example_failed, called().with_args(self.example))

        with it('increases failed counter'):
            expect(self.reporter.failed_count).to.be.equal(1)

        with it('keeps failed example'):
            self.reporter.example_failed(self.example)

            expect(self.reporter.failed_examples).to.have(self.example)

    #TODO: Pending
    #def it_notifies_event_example_pending_to_listeners():
    #    _.reporter.example_pending(_.example)

    #    assert_that(_.formatter.example_pending, called().with_args(_.example))

    #TODO: Pending
    #def it_increases_pending_counter_when_example_started():
    #    _.reporter.example_pending(_.example)

    #    expect(_.reporter.pending_count).to.be.equal(1)

    with context('when reporting events for an example group'):
        with before('each'):
            self.example_group = an_example_group()

        with it('notifies event example group started to listeners'):
            self.reporter.example_group_started(self.example_group)

            assert_that(self.formatter.example_group_started, called().with_args(self.example_group))

        with it('notifies event example group finished to listeners'):
            self.reporter.example_group_finished(self.example_group)

            assert_that(self.formatter.example_group_finished, called().with_args(self.example_group))

    #TODO: Pending
    #    def it_notifies_event_example_group_pending_to_listeners():
    #        _.example_group = a_pending_example_group()

    #        _.reporter.example_group_pending(_.example_group)

    #        assert_that(_.formatter.example_group_pending, called().with_args(_.example_group))

    with context('when finishing'):
        with it('notifies summary to listeners'):
            self.reporter.finish()

            assert_that(self.formatter.summary, called().with_args(
                self.reporter.duration,
                self.reporter.example_count,
                self.reporter.failed_count,
                self.reporter.pending_count
            ))

        with it('notifies failed examples to listeners'):
            self.reporter.finish()

            assert_that(self.formatter.failures, called().with_args(
                self.reporter.failed_examples
            ))
