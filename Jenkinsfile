pipeline {
    agent none

    stages {
        stage("Review") {
            when {
                expression { env.CHANGE_ID != null }
            }
            steps {
                node("slave-sbt") {
                    checkout scm
                    sh 'sbt clean scalafmtCheck scalafmtSbtCheck scapegoat test'
                }
            }
        }
        stage("Release") {
            when {
                expression { env.CHANGE_ID == null }
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
