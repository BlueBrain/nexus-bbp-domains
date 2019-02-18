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
                        sh 'ls -al /opt/rh/rh-python36/root/bin'
                        sh '$PYTHONPATH/python -m pip install git+https://github.com/BlueBrain/nexus-cli'
                        sh 'nexus --help'
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
