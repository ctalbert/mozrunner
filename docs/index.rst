:mod:`mozrunner` --- Reliable start/stop/configuration of Mozilla Applications
==============================================================================

.. module:: mozrunner
   :synopsis: Reliably starts/stops/configures XULRunner applications.
.. moduleauthor:: Mikeal Rogers <mikeal.rogers@gmail.com>
.. sectionauthor:: Mikeal Rogers <mikeal.rogers@gmail.com>

Profile Handling and Modification
---------------------------------

.. class:: Profile([default_profile[, profile[, create_new[, plugins[, preferences]]]]])

   XULRunner Application Profile Handling.

   *default_profile* is the location of the clean profile used by the application to 
   create new profiles. If one is not provided :meth:`find_default_profile()` will be called
   and that profile used.

   *create_new* instructs the init to create a new profile in a tmp diretory from the 
   *default_profile*. Defaults to :const:`True`.

   *profile* is the location of the profile you would like to use. *create_new* must be set to 
   :const:`False` in order to use this.

   *plugins* is a :class:`list` of plugins to install in to the profile. You can use paths to 
   directories containing extracted plugins or .xpi files which will b extracted and
   installed.

   *preferences* is a :class:`dict` of additional preferences to be set in the profile.
   Most Profile subclasses have a class member named "preferences", this is copied
   during initialization of the instance and updated with the *preferences* passed to 
   the constructor.
   
   .. attribute:: names
   
   :class:`list` of product names in order of priority. Not present by default, must 
   be defined in subclass.
   
   .. attribute:: preferences
   
   The default preferences :class:`dict`. If another preferences :class:`dict` is passed to
   the constructor this default will be copied and then updated.

   .. method:: find_default_profile()

   Finds the default profile location. Uses :attr:`names` .
	
   There is currently a bug in the Windows code: It's currently hardcoded to Firefox.

   .. method:: create_new_profile(default_profile_location)
	
   Creates a new profile in tmp and returns the path.
	
   *default_profile* is the path to the default profile described in the class docs
   above.

   .. method:: install_plugin(plugin)
	
   Installs a plugin in the profile. 
	
   *plugin* is a path to either an extracted addon or a .xpi .
	
   .. method:: set_preferences(preferences)
	
   Takes a :class:`dict`, *preferences*, and converts it to JavaScript `set_pref()` calls
   written to the profile's user.js .
	
   .. method:: clean_preferences()
	
   Cleans any preferences installed by mozunner from the profile.
	
   .. method:: clean_plugins()
	
   Removes all plugins installed by mozrunner from the profile.
	
   .. method:: cleanup()
	
   Triggers all cleanup operations. If a new profile was created in tmp it will
   remove the entire directory tree, if not it will call :meth:`clean_preferences()` and 
   :meth:`clean_plugins()`.

.. class:: FirefoxProfile([default_profile[, profile[, create_new[, plugins[, preferences]]]]])

   Firefox specific subclass of :class:`Profile`.

Process Run and Environment Handling and Discovery
--------------------------------------------------

.. class:: Runner([binary[, profile[, cmdargs[, env[, aggressively_kill[, kp_kwargs]]]]]])

   Handles all running operations. Finds binary, starts and stops the process.

   *binary* is the path to the application binary. If it is not specified 
   :meth:`find_binary()` will be used to find the product binary.
   
   *profile* is a :class:`Profile` instance. If not specified one will be created, 
   :attr:`profile_class` is used, no arguments are passed to it's constructor.
   
   *cmdargs* are additional command line arguments that will be added to the 
   subprocess call. Defaults to `[]`
   
   *env* is a :class:`dict` containing all the environment variables to be used in the
   subprocess call. Defaults to a copy of `os.environ` with `{"MOZ_NO_REMOTE":"1"}`
   added.
   
   *aggressivel_kill* is a :class:`list` of additional process names that need to be killed
   after killing the product. Defaults to `["crashreporter"]`.
   
   *kp_kwargs* the additional arguments sent to `killablleprocess.Popen`. Defaults to `{}`.
   
   .. attribute:: names
   
   List of product names in order of priority. Not present by default, must be defined in 
   subclass.
   
   .. attribute:: profile_class
   
   The default class to use when creating a new profile when one isn't passed to the 
   constructor.
   
   .. attribute:: command
   
   The command :class:`list` for subprocess. Not usually that usable without having the 
   instance, it's more common to use :func:`property` for attribute. Does not need to include 
   *cmdargs* sent to the constructor, those will be added later.
   
   .. method:: find_binary()

   Finds the binary location. Uses :attr:`names` for lookup names.
	
   There is currently a bug in the Windows code: It's currently hardcoded to Firefox.
   
   .. method:: start()
   
   Starts the subprocess call and sets :attr:`process_handler` to the returned 
   subprocess handler.
   
   .. method:: wait()
   
   Blocks and waits for the process to exit.
   
   .. method:: kill()
   
   Kills the application. This call is very aggressive, it kills all process id's 
   that are higher than the original pid if the one of the :attr:`names` is in the
   process name.
   
   .. method:: stop()
   
   Friendly pointer to :meth:`kill()`
   
.. class:: FirefoxRunner([binary[, profile[, cmdargs[, env[, aggressively_kill]]]]])

   Firefox specific subclass of :class:`Runner`.

Command Line Customization and Modification
-------------------------------------------
   
.. class:: CLI()
   
   Command Line Interface 
   
   .. attribute:: parser_options
   
   :class:`dict` of :class:`optparse.OptionParser` option definitions. Keys are 
   tuples with the short and long argument name definitions. Values must be 
   a keyword argument :class:`dict`::
   
      class SubCLI(CLI):
          parser_options = copy.copy(CLI.parser_options)
          parser_options[('f', '--file')] = {"default":None, "dest":"file", "help":"Log file name."}

   .. attribute:: parser
   
   Instace of :class:`optparse.OptionParser`. Created during instance initialiation.

   .. attribute:: runner_class
   
   Default runner class. Should be subclass of :class:`Runner`.
   Defaults to :class:`FirefoxRunner`. 

   .. attribute:: profile_class
   
   Default profile class. Should be subclass of :class:`Profile`.
   Defaults to :class:`FirefoxProfile`.
   
   .. method:: parse_and_get_runner()
   
   Responsible for calling :attr:`parser`.parse_args() and setting 
   :attr:`options` and :attr:`args`. Then responsible for calling
   :meth:`get_profile` and :meth:`get_runner` with parsed args from 
   :attr:`options` and returns the runner instance. Default implementation::
   
      def parse_and_get_runner(self):
           """Parses the command line arguments and returns a runner instance."""
           (options, args) = self.parser.parse_args()
           self.options  = options
           self.args = args
           if self.options.plugins is None:
               plugins = []
           profile = self.get_profile(default_profile=options.default_profile, 
                                      profile=options.profile, create_new=options.create_new,
                                      plugins=plugins)
           runner = self.get_runner(binary=self.options.binary, 
                                    profile=profile)
           return runner

   .. attribute:: options
   
   Options object returned from :attr:`parser`.parse_args(). :meth:`parse_and_get_runner()`
   is responsible for setting this attribute before calling :meth:`get_profile` and 
   :meth:`get_runner`.
   
   .. attribute:: args
   
   Args :class:`list` returned from :attr:`parser`.parse_args(). 
   :meth:`parse_and_get_runner()` is responsible for setting this attribute before calling 
   :meth:`get_profile` and :meth:`get_runner`.
   
   .. method:: get_profile([default_profile[, profile[, create_new[, plugins]]]])
   
   Takes arguments as parsed from :attr:`options` and returns an instance of 
   :attr:`profile_class`
   
   .. method:: get_runner([binary[, profile]])
   
   Takes arguments as parsed from :attr:`options` and the profile instance returned from
   :meth:`get_profile` and returns an instance of :attr:`runner_class`.
   
   .. method:: start(runner)
   
   Starts the runner and waits for :meth:`Runner.wait()` or :exc:`KeyboardInterrupt`.
   
   .. method:: run()
   
   Calls :meth:`parse_and_get_runner` and passes the returned value to :meth:`start`.

Examples
========

Firefox subclasses::

   class FirefoxProfile(mozrunner.Profile):
       """Specialized Profile subclass for Firefox"""
       preferences = {'extensions.update.enabled'    : False,
                      'extensions.update.notifyUser' : False,
                      'browser.shell.checkDefaultBrowser' : False,
                      'browser.tabs.warnOnClose' : False,
                      'browser.warnOnQuit': False,
                      'browser.sessionstore.resume_from_crash': False,
                      }

       @property
       def names(self):
           if sys.platform == 'darwin':
               return ['firefox', 'minefield', 'shiretoko']
           if sys.platform == 'linux2':
               return ['firefox', 'mozilla-firefox', 'iceweasel']
           if os.name == 'nt' or sys.platform == 'cygwin':
               return ['firefox']

   class FirefoxRunner(mozrunner.Runner):
       """Specialized Runner subclass for running Firefox."""
       @property
       def names(self):
           if sys.platform == 'darwin':
               return ['firefox', 'minefield', 'shiretoko']
           if sys.platform == 'linux2':
               return ['firefox', 'mozilla-firefox', 'iceweasel']
           if os.name == 'nt' or sys.platform == 'cygwin':
               return ['firefox']

