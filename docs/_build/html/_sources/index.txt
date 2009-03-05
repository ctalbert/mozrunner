:mod:`mozrunner` --- Browser Automation Tool
===========================================

.. module:: mozrunner
   :synopsis: Reliably starts/stops/configures XULRunner applications.
.. moduleauthor:: Mikeal Rogers <mikeal.rogers@gmail.com>
.. sectionauthor:: Mikeal Rogers <mikeal.rogers@gmail.com>

.. class:: Profile([default_profile[, profile[, create_new[, plugins[, preferences]]]]])

   XULRunner Application Profile Handling.

   *default_profile* is the location of the clean profile used by the application to 
   create new profiles. If one is not provided :meth:`find_default_profile()` will be called
   and that profile used.

   *create_new* instructs the init to create a new profile in a tmp diretory from the 
   *default_profile*. Defaults to `True`.

   *profile* is the location of the profile you would like to use. *create_new* must be set to 
   False in order to use this.

   *plugins* is a list of plugins to install in to the profile. You can use paths to 
   directories containing extracted plugins or .xpi files which will b extracted and
   installed.

   *preferences* is a dictionary of additional preferences to be set in the profile.
   Most Profile subclasses have a class member named "preferences", this is copied
   during initialization of the instance and updated with the *preferences* passed to 
   the constructor.
   
   .. attribute:: names
   
   List of product names in order of priority. Not present by default, must be defined in 
   subclass.
   
   .. attribute:: preferences
   
   The default preferences dictionary. If another preferences dictionary is passed to
   the constructor this default dict will be copied and then updated.

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
	
   Takes a dictionary, *preferences*, and converts it to JavaScript `set_pref()` calls
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

.. class:: Runner([binary[, profile[, cmdargs[, env[, aggressively_kill]]]]])

   Handles all running operations. Finds binary, starts and stops the process.

   *binary* is the path to the application binary. If it is not specified 
   :meth:`find_binary()` will be used to find the product binary.
   
   *profile* is a :class:`Profile` instance. If not specified one will be created, 
   :attr:`profile_class` is used, no arguments are passed to it's constructor.
   
   *cmdargs* are additional command line arguments that will be added to the 
   subprocess call. Defaults to `[]`
   
   *env* is a dictionary containing all the environment variables to be used in the
   subprcoess call. Defaults to to a copy of `os.environ` with `{"MOZ_NO_REMOTE":"1"}`
   added.
   
   *aggressivel_kill* is a list of additional process names that need to be killed
   after killing the product. Defaults to `["crashreporter"]`.
   
   .. attribute:: names
   
   List of product names in order of priority. Not present by default, must be defined in 
   subclass.
   
   .. attribute:: profile_class
   
   The default class to use when creating a new profile when one isn't passed to the 
   constructor.
   
   .. attribute:: command
   
   The command list for subprocess. Not usually that usable without having the instance, 
   it's more common to use `@property` for attribute. Does not need to include *cmdargs* 
   sent to the constructor, those will be added later.
   
   .. method:: find_binary()

   Finds the binary location. Uses :attr:`names` for lookup names.
	
   There is currently a bug in the Windows code: It's currently hardcoded to Firefox.
   
   .. method:: start()
   
   Starts the subprocess call and sets :attr:`process_handler` to the returned 
   subprocess handler.
   
   .. method:: wait()
   
   Blocks and waits for the call to exit.
   
   .. method:: kill()
   
   Kills the application. This call is very aggressive, it kills all process id's 
   that are higher than the original pid if the one of the :attr:`names` is in the
   process name.
   
   .. method:: stop()
   
   Friendly pointer to :meth:`kill()`
   
.. class:: FirefoxRunner([binary[, profile[, cmdargs[, env[, aggressively_kill]]]]])

   Firefox specific subclass of :class:`Runner`.
   
   








