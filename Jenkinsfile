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
           input {
                message "Proceed ?"
                ok "Ok"
                parameters {
                    string(name: 'org', defaultValue: 'neurosciencegraph', description: 'organization')
                    string(name: 'project', defaultValue: 'datamodels', description: 'project')
                    string(name: 'strategy', defaultValue: 'UPDATE_IF_DIFFERENT', description: 'Schema import strategy')
                    string(name: 'nexusenv',, defaultValue: 'nexusenv', description: 'nexusenv')
                    string(name: 'token', defaultValue: 'token', description: 'Token')
                }
            }
            steps {
                node("slave-sbt") {
                    withEnv(['PYTHONPATH=/opt/rh/rh-python36/root/bin','LC_CTYPE=en_US.UTF-8']) {
                        sh  '$PYTHONPATH/python -V'
                        checkout scm
                        
                        
                        sh '$PYTHONPATH/python -m venv bbpdomains'
                        sh 'source bbpdomains/bin/activate'
                        sh 'bbpdomains/bin/pip3 install git+https://github.com/BlueBrain/nexus-cli'
                        sh 'sbt clean scalafmtCheck scalafmtSbtCheck scapegoat test'
                        sh 'sbt copyResourcesFromJar'
                        sh 'ls -al target'
                        sh 'bbpdomains/bin/nexus --help'
                        sh "bbpdomains/bin/nexus profiles create ${nexusenv} ${nexusenv}"
                        sh "bbpdomains/bin/nexus profiles select ${nexusenv}"
                        sh "bbpdomains/bin/nexus auth  set-token ${token}"
                        sh "bbpdomains/bin/nexus schemas create --org ${org} --project ${project} --dir target/shapes/neurosciencegraph/datashapes -n https://neuroshapes.org/dash --strategy ${strategy} -b \"{\"https://provshapes.org/dash\": \"target/shapes/prov/datashapes\",\"https://provshapes.org/commons\": \"target/shapes/prov/commons\",\"https://neuroshapes.org/dash\": \"target/shapes/neurosciencegraph/datashapes\",\"https://neuroshapes.org/commons\": \"target/shapes/neurosciencegraph/commons\"}"
                        
                        
                        
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
