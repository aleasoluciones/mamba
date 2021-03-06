from expects import expect
from doublex import Spy

from spec.object_mother import *

from mamba import reporter
from mamba.example_group import ExampleGroup


with description(ExampleGroup):

    with before.each:
        self.example_group = an_example_group()
        self.reporter = Spy(reporter.Reporter)

    with it('has same name than subject'):
        expect(self.example_group.name).to.be(IRRELEVANT_SUBJECT)

    with context('when run'):

        with before.each:
            self.example = an_example()
            self.example_group.append(self.example)

            self.example_group.run(self.reporter)

        with it('runs the example'):
            expect(self.example.was_run).to.be.true

        with it('calculates elapsed time'):
            expect(self.example_group.elapsed_time.total_seconds()).to.be.above(0)

        with it('notifies that an example group was started'):
            expect(self.reporter.example_group_started).to.have.been.called.with_args(self.example_group)

        with it('notifies that an example group is finished'):
            expect(self.reporter.example_group_finished).to.have.been.called.with_args(self.example_group)

    with context('when run failed'):

        with before.each:
            self.example_group.append(a_failing_example())

            self.example_group.run(self.reporter)

        with it('is marked as failed'):
            expect(self.example_group.failed).to.be.true

    with context('when before all hook raises an error'):
        with before.each:
            class _ErrorRaiser(object):
                def _raise_error(self):
                    raise ValueError()
            #TODO: Law of Demeter!
            #_.example_group.add_hook('before_all', _raise_error)
            self.example_group.hooks['before_all'] = []
            self.example_group.hooks['before_all'].append(_ErrorRaiser._raise_error)


        with context('when has only examples as children'):
            with before.each:
                self.example_group.append(an_example())

                self.example_group.run(self.reporter)

            with it('maks failed all children'):
                expect(self.example_group.examples[0].failed).to.be.true

            with it('propagates error to all children'):
                expect(self.example_group.examples[0].error).to.not_be.none

            with it('does not execute any example'):
                expect(self.example_group.examples[0].was_run).to.be.false

            with it('report child example as failed'):
                expect(self.reporter.example_failed).to.have.been.called.with_args(self.example_group.examples[0])

        with context('when has contexts as children'):
            with before.each:
                self.example_group.append(an_example_group())
                self.example_group.examples[0].append(an_example())

                self.example_group.run(self.reporter)

            with it('marks failed all children in context'):
                expect(self.example_group.examples[0].failed).to.be.true

            with it('propagates error to all children in context'):
                expect(self.example_group.examples[0].error).to.not_be.none
