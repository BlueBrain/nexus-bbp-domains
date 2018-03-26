def version = env.BRANCH_NAME

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
        stage("Build Image") {
            when {
                expression { env.CHANGE_ID == null && version ==~ /v\d+\.\d+\.\d+.*/ }
            }
            steps {
                node("slave-sbt") {
                    checkout scm
                    sh "sbt clean paradox universal:packageZipTarball"
                    sh "mv target/universal/bbp-domains-docs.tgz ."
                    sh "oc start-build domains-build --from-file=bbp-domains-docs.tgz --follow"
                    openshiftTag srcStream: 'domains', srcTag: 'latest', destStream: 'domains', destTag: version.substring(1), verbose: 'false'
                }
            }
        }
    }
}
