#!/usr/bin/env bash
#author: hasha@redhat.com

#Ge the API token following these steps:
#    Log in to Jenkins.
#    Click your name (upper-right corner).
#    Click Configure (left-side menu).
#    Click Show API Token.
#The API token is revealed.
#You can change the token by clicking the Change API Token button.
#export JENKINS_USER_ID=$user_id
#export JENKINS_USER_TOKEN=$token

#set -o errexit
set -o nounset
set -o pipefail


print_usage() {
echo "$(basename "$0") - Generate cucushift vars
Usage: $(basename "$0") [options...]
Options:
  jenkins  If specified, will trigger runner-v3 jenkins job.
  dry-run          If specified, only print the vars that would be used by cucushift, without updating your shell script. (If you are first time to use the script, suggest copy the result of dryrun to your own var script. Ever since you can use --update-file directly)
  update-file|-update  The script will update your exsiting var shell script you specified. Suggest you use the \$source(or .) cucushift_var.sh to run the script.
" >&2
}

update_file() {
    echo "input the path of your shell script:  (you can fix the value of shell_path, no need to input the shell_path everytime)"
    read shell_path
    sed -i -r "/ENV_OCP4_HOSTS/s/([a-Z|/b]+=)(.*)/\1$MARSTER:master:node,$LB:lb/" $shell_path
    sed -i -r "/ENV_OCP4_USER_MANAGER_USERS/s/([a-Z|/b]+=)(.*)/\1$users/" $shell_path
    sed -i -r "/admin_creds_spec/s|([a-Z|/b]+:)(.*)|\1 \"$KUBE_VIEWLINK\"|" $shell_path
    sed -i -r "/version/s/([a-Z|/b]+:)(.*)/\1 \"$VERSION\"/" $shell_path
    sed -i -r "/idp/s|([a-Z|/b]+:)(.*)|\1 \"$IDP\"|"  $shell_path
    sed -i -r "/admin_console_url/s|([a-Z|/b]+:)(.*)|\1 \"$CONSOLE_ROUTE\"|" $shell_path
    source $shell_path
    echo "Your cucushift envvars has been sourced if you run script by source command, you can run case directly!"

}
generate_cucushift_vars() {

  echo "+++++++++++++++++++++++cucushift variables+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  echo "export BUSHSLICER_DEBUG_AFTER_FAIL=1"
  echo "export BUSHSLICER_DEFAULT_ENVIRONMENT=ocp4"
  echo "export OPENSHIFT_ENV_OCP4_HOSTS=$hosts"
  echo "export OPENSHIFT_ENV_OCP4_USER_MANAGER_USERS=$users"
  echo "export BUSHSLICER_CONFIG='
  global:
    browser: chrome
  environments:
    ocp4:
      admin_creds_spec: \"$KUBE_VIEWLINK\"
      version: \"$VERSION\"
      idp: \"flexy-htpasswd-provider\"
      admin_console_url: \"$CONSOLE_ROUTE\"
'
"
 
}

init_cluster_var() {

  read -p "Please input cluster job link(looks like https://openshift-qe-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/job/Launch%20Environment%20Flexy/76748): " JOB_LINK
  JOB_LINK=`echo $JOB_LINK|cut -d '/' -f 1-6`
  KUBE_VIEWLINK=$JOB_LINK"/artifact/workdir/install-dir/auth/kubeconfig/*view*/"
  USER_VIEWLINK=$JOB_LINK"/artifact/users.spec/*view*/"
  HOST_VIEWLINK=$JOB_LINK"/artifact/host.spec/*view*/"
  curl -k -o ./cucushift_kubeconfig $KUBE_VIEWLINK &> /dev/null
  curl -k -o ./cucushift_users $USER_VIEWLINK &> /dev/null
  hosts=`curl $HOST_VIEWLINK 2> /dev/null`
  num=$((RANDOM%50))
  users=$(cat ./cucushift_users | awk -F, 'OFS="," {print $"'$num'",$("'$num'"+1)}')
  echo "you will use these two users: $users"
  VERSION=`oc get clusterversion --config=./cucushift_kubeconfig | awk 'NR==2{print $2}' | cut -d. -f 1-2`
  CONSOLE_ROUTE=$(oc get route -n openshift-console --config=./cucushift_kubeconfig | awk  '$1 ~ /console/{print "https://"$2}')
  MARSTER=$(oc get node -l node-role.kubernetes.io/master --config=./cucushift_kubeconfig | awk 'NR==2{print $1}')
  LB=$(oc get infrastructures.config.openshift.io cluster -o 'jsonpath={.status.apiServerURL}' --config=./cucushift_kubeconfig | sed -e 's|^[^/]*//||' -e 's|:.*$||')
  IDP=flexy-htpasswd-provider
  rm ./cucushift_kubeconfig
  rm ./cucushift_users

}

generate_jenkins_paramters() {
  read -p "Please input cases/testrun(OCP-12345,OCP-123456 Or 20200109-0015): " cases
  [[ $cases == OCP* ]] && tcms_spec=cases:$cases || tcms_spec=testrun:$cases
  default_env=ocp4
  log_level=INFO
  repo_owner=openshift
  repo_branch=master
  tierN_repo_owner=openshift
  tierN_repo_branch=master
  read -p "Change the repo owner/branch [default: openshift/master]? (y/n):" change_repo
  if [[ $change_repo =~ [y|Y].* ]]; then
      read -p "repo owner: " repo_owner
      read -p "branch: " repo_branch
      read -p "tierN repo owner: " tierN_repo_owner
      read -p "tierN repo branch: " tierN_repo_branch
  fi
  label_expression=`echo "cucushift && oc$VERSION" |tr -d .`
  test_mode=non-destructive

} 

launch_jenkins_job() {
  export JENKINS_USER_ID=hasha
  export JENKINS_USER_TOKEN=24e28235800ed09f597ad259cd39b53c
  export tcms_spec default_env hosts users log_level repo_owner repo_branch tierN_repo_owner tierN_repo_branch label_expression test_mode
  export config=`echo "
  global:
    browser: chrome
  environments:
    ocp4:
      admin_creds_spec: \"$KUBE_VIEWLINK\"
      version: \"$VERSION\"
      idp: \"flexy-htpasswd-provider\"
      admin_console_url: \"$CONSOLE_ROUTE\"
"`

  python <<EOF
import jenkins_server,os;

job_name = "Runner-v3"
build_launch_vars = dict()
build_launch_vars["TCMS_SPEC"] =  os.environ['tcms_spec']
build_launch_vars["BUSHSLICER_DEFAULT_ENVIRONMENT"] =  os.environ['default_env']
build_launch_vars["HOSTS"] =  os.environ['hosts']
build_launch_vars["USERS"] =  os.environ['users']
build_launch_vars["BUSHSLICER_CONFIG"] =  os.environ['config']
build_launch_vars["BUSHSLICER_LOG_LEVEL"] =  os.environ['log_level']
build_launch_vars["REPO_OWNER"] =  os.environ['repo_owner']
build_launch_vars["BRANCH"] =  os.environ['repo_branch']
build_launch_vars["TIERN_REPO_OWNER"] =  os.environ['tierN_repo_owner']
build_launch_vars["TIERN_REPO_BRANCH"] =  os.environ['tierN_repo_branch']
build_launch_vars["LABEL_EXPRESSION"] =  os.environ['label_expression']
build_launch_vars["TEST_MODE"] =  os.environ['test_mode']

print("**************************************************************************")
print("Trigger Jenkins Runner-v3 Job.......................waiting...")

ret = jenkins_server.run_job(job_name, build_launch_vars)

print("Jenkins job link: https://openshift-qe-jenkins.rhev-ci-vms.eng.rdu2.redhat.com/job/Runner-v3/"+str(ret["build_num"])+"/console")
if ret["status"]:
    print("Your job PASSED!")
else:
    print("Your job FAILED!")


EOF
}

for i in "$@"
do
case $i in
    dry-run)
    init_cluster_var	    
    generate_cucushift_vars
    ;;
    -h|--help)
      print_usage
    ;;
    -update|update-file)
      init_cluster_var
      update_file
    ;;
    jenkins)
      init_cluster_var
      generate_jenkins_paramters
      launch_jenkins_job
    ;;
    *)
     print_usage
    ;;
esac
done

   
