# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s iuem20.project -t test_project.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src iuem20.project.testing.IUEM20_PROJECT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_project.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a project
  Given a logged-in site administrator
    and an add project form
   When I type 'My project' into the title field
    and I submit the form
   Then a project with the title 'My project' has been created

Scenario: As a site administrator I can view a project
  Given a logged-in site administrator
    and a project 'My project'
   When I go to the project view
   Then I can see the project title 'My project'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add project form
  Go To  ${PLONE_URL}/++add++project

a project 'My project'
  Create content  type=project  id=my-project  title=My project


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the project view
  Go To  ${PLONE_URL}/my-project
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a project with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the project title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
