<template>
  <q-dialog v-model="is_open" persistent>
    <q-layout view="Lhh lpR fff" container class="bg-white" style="width: 900px; max-width: 80vw;">
      <q-header class="bg-primary">
        <q-toolbar>
          <q-toolbar-title>
            Welcome to Redirectory! <i class="text-grey-6">User Guide</i>
          </q-toolbar-title>
          <q-btn flat v-close-popup round dense icon="close"/>
        </q-toolbar>
        <div class="bg-primary flex flex-center" style="margin-bottom: 5px">
          <a href="#rules">
            <q-chip color="secondary" text-color="white" clickable>
              Rules
            </q-chip>
          </a>
          <a href="#redirect-rules">
            <q-chip color="secondary" text-color="white" clickable>
              Redirect Rule Explorer
            </q-chip>
          </a>
          <a href="#bulk">
            <q-chip color="secondary" text-color="white" clickable>
              Bulk Import
            </q-chip>
          </a>
          <a href="#ambiguous">
            <q-chip color="secondary" text-color="white" clickable>
              Ambiguous requests
            </q-chip>
          </a>
          <a href="#hyperscan">
            <q-chip color="secondary" text-color="white" clickable>
              Hyperscan DB
            </q-chip>
          </a>
          <a href="#workers">
            <q-chip color="secondary" text-color="white" clickable>
              Workers and Kubernetes
            </q-chip>
          </a>
        </div>
        <q-separator class="toolbarGradient"/>
      </q-header>

      <q-page-container>
        <q-page padding style="padding-top: 5px !important;">
          <!-- DOCS -->
          <div class="text-primary text-h6 text-bold">
            Overview
          </div>
          <q-separator class="userGuide"/>
          <p class="text-subtitle1" style="margin-top: 10px">
            <q-separator class="separatorHidden"></q-separator>
            This is a piece of software for redirecting requests
            that would usually end up with a 404 response to a new destination specified by
            given rules. It is made to work and take advantage of a Kubernetes environment.
            What you are currently looking at is the so called "management panel" or whatever you
            <i id="rules"></i>
            would like to call it. <br>
            <q-separator class="separatorHidden"></q-separator>
            From here you can manage amd access all of the features provided by Redirectory.
            This User Guide aims to show you how you can use it!
            Lets begin with the rules.
          </p>

          <div class="text-primary text-h6 text-bold">
            Rules
          </div>
          <q-separator class="userGuide"/>
          <div class="text-subtitle1" style="margin-top: 10px">
            Rules are the main things that tells Redirectory how to redirect the incoming requests.
            This section will show you how to
            <ol>
              <li>
                Create new rules
              </li>
              <li>
                Edit existing rules
              </li>
              <li>And delete not needed once</li>
            </ol>
            In order for it to redirect lets say: <br>
            <q-separator class="separatorHidden"></q-separator>
            <div class="doc-note text-primary">
              <p>
                &emsp; https://old.example.com/<b class="text-accent">.*</b> -> to -> https://new.example.com/ <br>
              </p>
            </div>
            <q-separator class="separatorHidden"></q-separator>
            we will first need to enter a rule for this. First you will have
            to go to the Redirect Rule Explorer section. <br>
            There underneath the search
            filters you will find a button just like this one:
            <q-btn color="primary" icon="add" label="CREATE NEW REDIRECT RULE" style="margin-right: 10px"></q-btn>
            <br>
            Once clicked a menu with a few options will appear. The first thing to specify is
            the domain you would like to redirect from. Keep in mind this domain should be configured
            that it points to the cluster you are using Redirectory in. After you are done with the domain
            it should look something like this:
            <div style="padding: 10px" class="flex flex-center">
              <img src="statics/create_domain.png" style="max-width: 90%">
            </div>
            The next thing we need to configure is the path of the domain we just added. Lets to this one the
            same way as the domain. You might have noticed that we have a (<b class="text-accent">.*</b>) in
            the path of the rule. <br>
            This is called <b class="text-primary">Regex</b> and it is one of the features of Redirectory, If you have
            a regex expression you need to toggle the button that looks like this:
            <q-toggle
              :label="path_is_regex"
              v-model="path_is_regex"
              checked-icon="code"
              unchecked-icon="text_format"
              false-value="LITERAL"
              true-value="REGEX"
              color="secondary"
              class="toggle-label"
            />
            See a little bit more info on Regex in the note below.
            <div class="doc-note text-primary" style="margin-bottom: 5px">
              <p class="doc-note__title">REGEX</p>
              Regex quite an expansive topic we don't need much to be able to use it.
              It is used to select text and in our case URLs. Here are most of the things you will
              need to get started:
              <ol class="text-bold">
                <li><b class="text-accent">.</b> - any character</li>
                <li><b class="text-accent">\d</b> - just numbers</li>
                <li><b class="text-accent">\w</b> - just letters</li>
                <li><b class="text-accent">*</b> - zero or more</li>
                <li><b class="text-accent">+</b> - one or more</li>
              </ol>
              Now we can chain them together like this:
              <p class="text-bold">
                &emsp; /test/path<b class="text-accent">.*</b>
              </p>
              which will match any of those:
              <p class="text-bold">
                &emsp; /test/path/any <br>
                &emsp; /test/path/of <br>
                &emsp; /test/path/those <br>
                &emsp; /test/path/123 <br>
              </p>
            </div>
            Now that we now what we are actually typing in we can fill it in and it should look
            like the following:
            <div style="padding: 10px" class="flex flex-center">
              <img src="statics/create_path.png" style="max-width: 90%">
            </div>
            You can fill in the destination the exact same way we did the first two. The last thing
            that needs to be configured is the weight of a rule. Why do we need it? Sometimes you
            <i id="redirect-rules"></i>
            can get conflicting rules that both of them match the same request. When this happens Redirectory
            has to know which rules has bigger weight (priority). This is expressed with the weight value
            of the rule. By default all rules get a weight of 100. <br>
            Now we can just create the rule with the following button:
            <q-btn color="green" @click="create()">CREATE</q-btn>
          </div>

          <div class="text-primary text-h6 text-bold">
            Redirect Rule Explorer
          </div>
          <q-separator class="userGuide"/>
          <div class="text-subtitle1" style="margin-top: 10px">
            With the Explorer you have all the things you would need in order to manage all
            of the Redirect Rules for Redirectory. Like we discussed in the Rules section here
            you can create a new rule but also much more. <br>
            <q-separator class="separatorHidden"></q-separator>
            On top are the filters. With them you can search through all of the rules you have.
            You can stack multiple filters to narrow down your search even more. Also keep in mind
            that for the domain, path and destination filters you can use (*) which is an fnmatch.
            <q-separator class="separatorHidden"></q-separator>
            <div class="doc-note text-primary" style="margin-bottom: 5px">
              <p class="doc-note__title">FNMATCH</p>
              FNMATCH or also called Function Match is a way simpler form of regex. Basically you
              can have a (*) which is equivalent to (.+) in Regex and and will match one or more.
            </div>
            <q-separator class="separatorHidden"/>
            After you set the filters just press the button:
            <q-btn color="primary" icon="search" label="APPLY FILTERS"></q-btn>
            <br>
            <q-separator class="separatorHidden"/>
            Once you have located the rule that you want in order to view it, edit or delete it you
            can just click on it: Then the following options will be given for that rule:
            <i id="bulk"></i>
            <div style="padding: 10px" class="flex flex-center">
              <img src="statics/explorer_rule.png" style="max-width: 102%">
            </div>
            Keep in mind the rules are not updated automatically in the User Interface. To make sure
            your are seeing the latest changes to the rules please click the refresh button:
            <q-btn color="secondary" icon="refresh" label="REFRESH PAGES"></q-btn>
          </div>

          <div class="text-primary text-h6 text-bold">
            Bulk Import
          </div>
          <q-separator class="userGuide"/>
          <div class="text-subtitle1" style="margin-top: 10px">
            But what if I have a lot of rules? For this situation you can make use of the bulk import
            feature. With it you can upload a CSV (Coma Separated Values) file and all of the rules
            will be added at once. Because CSV is a basic format a lot of programs support an export to it.
            You will have to refer to the documentation of the program you are using for more information on
            exporting the data as CSV. <br>
            <q-separator class="separatorHidden"></q-separator>
            Take a look at the Bulk Import Section for more information on how the CSV file should be formated
            <i id="ambiguous"></i>
            in order to get the smooth import. <br>
            <q-separator class="separatorHidden"></q-separator>
            Once you have uploaded the file the import will begin immediately. The time it takes to process and add
            all the rules varies on how of course how many you have.
          </div>

          <div class="text-primary text-h6 text-bold">
            Ambiguous requests
          </div>
          <q-separator class="userGuide"/>
          <div class="text-subtitle1" style="margin-top: 10px">
            Ambiguous requests are requests for which Redirectory was unable to decide 100% of what
            should be the final destination. What does this mean? The main reason of you seeing
            ambiguous requests is that you have some rules that are not configured correctly. <br>
            <q-separator class="separatorHidden"></q-separator>
            Sometimes it happens that two or more rules intersect each other and Regex has trouble choosing
            which one is the more important one because all of them match. Example of intersection: <br>
            <div class="doc-note text-primary">
              <p>
                &emsp; <b>1.</b>&emsp; ggg.test.kumina.nl/test/path/<b class="text-accent">.*</b>
              </p>
              <p>
                &emsp; <b>2.</b>&emsp; <b class="text-accent">\w+</b>.test.kumina.nl/test/path/<b
                class="text-accent">.*</b>
              </p>
              <p>
                &emsp; <b>3.</b>&emsp; <b class="text-accent">.*</b>.test.kumina.nl/test/pa<b class="text-accent">.*</b>
              </p>
            </div>
            Now if we make a requests that looks like this: <br>
            <div class="doc-note text-primary">
              <p>
                <b>
                  &emsp; ggg.test.kumina.nl/test/path/aaabb
                </b>
              </p>
            </div>
            we will match all of the three rules and Redirectory will not know which one should it choose.
            When this happens Redirectory will always choose the first rule (with the smallest id) and it will
            also save the request as ambiguous in order for a person to take a look and change the weights of the
            rules in order not to happen again.
            <q-separator class="separatorHidden"></q-separator>
            You will be able to see the ambiguous requests section. There are a few options you can make use of in this
            section.
            On the top right there is the following button:
            <q-btn color="secondary" icon="refresh" label="RELOAD AMBIGUOUS REQUESTS"></q-btn>
            Once you click an entry/request you are presented with two options.
            Test option will put this request in the Test Section and show you what is happening
            behind the scenes. From there you can specify the correct weights for the rules in order
            to avoid any ambiguous requests in the future.
            Once you have fixed the issue for a given ambiguous request you can delete it with the
            second option. See image below for better understanding.
            <div style="padding: 10px" class="flex flex-center">
              <i id="hyperscan"></i>
              <img src="statics/ambiguous.png" style="max-width: 102%">
            </div>
          </div>

          <div class="text-primary text-h6 text-bold">
            Hyperscan Database
          </div>
          <q-separator class="userGuide"/>
          <i id="workers"></i>
          <div class="text-subtitle1" style="margin-top: 10px">
            You have probably noticed that when adding, updating and deleting a rule
            you have a message that say that the changes will not apply until you
            compile a new Hyperscan database. This is due to the backend and how Hyperscan works.
            First make all the changes you would like and then once you are done with all of them
            you can compile/create a new Hyperscan database.
            <q-separator class="separatorHidden"></q-separator>
            The settings are located in the Hyperscan Database and Workers Section.
            Now that you have made the changes you wanted to the rules you can press the:
            <q-btn color="accent" icon="launch" label="COMPILE NEW HS DB"></q-btn>
            button. This will create a new Hyperscan Database and apply it to all of the workers.
            That is everything you need to be worried about with Hyperscan. If you are interested
            in the workers and how they work please take a look at the next section in the User Guide.
          </div>

          <div class="text-primary text-h6 text-bold">
            Workers and Kubernetes
          </div>
          <q-separator class="userGuide"/>
          <div class="text-subtitle1" style="margin-top: 10px">
            Redirectory is an application that runs in Kubernetes and makes use of it's scaling features.
            That is why the application is split into two parts: <b>management</b> and <b>workers</b>.
            The workers are the one that process all of the incoming requests. That is why they need to
            be up to date with the newest version of the Hyperscan Database. In other words the Redirect Rules. <br>
            <q-separator class="separatorHidden"></q-separator>
            You will find all of the options for the management and workers in the Hyperscan Database and Workers
            Section.
            From there you can see the status of each worker and the current database they have loaded on them. This
            information
            updates automatically every 10 seconds or you can click the
            <q-btn round color="secondary" icon="refresh"></q-btn>
            button to update now.<br>
            <q-separator class="separatorHidden"></q-separator>
            The
            <q-btn color="accent" icon="launch" label="COMPILE NEW HS DB"></q-btn>
            button creates a new database and
            <b>updates all the workers</b> after that. If for some reason a worker is out of date you can use the:
            <q-btn color="primary" icon="update" label="UPDATE ALL"></q-btn>
            button or by clicking
            on the out of date worker and updating it individually. From there you can view the configuration
            of the workers as well. Take a look at the picture below:
            <div style="padding: 10px" class="flex flex-center">
              <img src="statics/workers.png" style="max-width: 102%">
            </div>
          </div>

          <q-footer class="bg-grey-3 text-black">
            <div class="text-center" style="padding-top: 2px; padding-bottom: 2px;">
              Documentation for developers can be seen here:
              <a href="https://redirectory.readthedocs.io">Redirectory Dev Docs</a>
            </div>
          </q-footer>
        </q-page>
      </q-page-container>
    </q-layout>
  </q-dialog>
</template>

<script>
export default {
  name: 'UserGuideDialog',
  computed: {
    is_open: {
      get: function () {
        return this.$store.state.dialogs.show_user_guide
      },
      set: function (value) {
        this.$store.commit('dialogs/set_user_guide', value)
      }
    }
  },
  data () {
    return {
      position: 'fullscreen',
      path_is_regex: 'LITERAL'
    }
  },
  methods: {
    close () {
      this.is_open = false
    },
    get_color (value) {
      return value ? 'text-positive' : 'text-negative'
    }
  }
}
</script>

<style scoped lang="stylus">
  .separatorHidden
    visibility hidden
    height 3px

  a
    text-decoration none
</style>
