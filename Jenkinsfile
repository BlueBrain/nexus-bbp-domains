String version = env.BRANCH_NAME
Boolean isRelease = version ==~ /v\d+\.\d+\.\d+.*/
Boolean isPR = env.CHANGE_ID != null

pipeline {
    agent none

    stages {
        stage("Review") {
            when {
                expression { isPR }
            }
            steps {
                node("slave-sbt") {
                    withEnv(['PYTHONPATH=/opt/rh/rh-python36/root/bin']) {
                        sh  '$PYTHONPATH/python -V'
                        checkout scm
                        sh 'pwd'
                        sh '$PYTHONPATH/python -m venv bbpdomains'
                        sh 'source bbpdomains/bin/activate'
                        sh 'bbpdomains/bin/pip3 install git+https://github.com/BlueBrain/nexus-cli'
                        sh 'echo $LC_ALL'
                        sh 'echo $LANG'
                        sh 'ls -al bbpdomains/bin'
                        sh ' bbpdomains/bin/nexus --help'
                        sh 'sbt clean scalafmtCheck scalafmtSbtCheck scapegoat test'
                    }

                }
            }
        }
        stage("Release") {
            when {
                expression { isRelease }
            }
            steps {
                node("slave-sbt") {
                    checkout scm
                    sh 'sbt clean releaseEarly'
                }
            }
        }
    }
}
