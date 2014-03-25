
[ecs]: https://github.com/seanfisk/ecs "ecs"
[pygame]: http://pygame.org/download.shtml "Pygame"


# PyTanks (name change pending)
Attempt at a (programmable) shoot'em up game based on an entity-component-system,
requires Python3, [pygame][] and [ecs][].

## Running
Grab [pygame][] from your favorite package manager and [ecs][] from PyPI (`pip
install ecs`).

Then `./bin/tanks/ demo` should create a window with a bit of stuff going on.  
There will be two turret shooting at things and a tank driving around doing
nothing in particular. You may have to squint a bit to recognize them as I may have
been a bit laz… abstract when designing the textures.  
So the twist is that this behaviour is not hardcoded into the demo but
controlled by (more or less) simple python coroutines. They are found in
[examples/](examples/), feel free to play around with them once I
have explained how they work.  
You can also have a number routines battle each other with `./bin/tanks match
path/script1.py path/script2.py …`. 

## Scripts
I'll just assume you know about python's function generators for now. The cool
thing about generators is that they allow us to start/stop execution at almost
arbitrary points in functions.  
The only constraints on you script files are:  
1. they contain valid python (this is why you want to watch whose scripts you
   run, nothing stops a script from running `shutil.rmtree ("~")`)  
2. they have a generator function called `main` which takes two arguments
   (which I'll explain later)  
3. they yield functions taking no arguments which return either `True` or
   `False`

The general process followed by the game is this:  
1. it calls `main` with an object representing the tank your script controls
   and an iterator over all other objects in the game, thereby instantiating
   the generator  
2. each tick of the game the function last yielded by your generator is
   executed (`lambda: True` in the first tick), if it returns `True` execution in
   your generator is resumed, if not the game will just retry in the next tick  
3. your generator runs until you yield the next function, during that period
   the game does *nothing* else, i.e. *between* `yields` everything is static,
   but also that malicious scripts can halt the whole game  
4. goto 2.   

So with that in mind let's look over
[examples/demo_tank.py](examples/demo_tank.py#L20) to get some of the details
straight.

* Line 20-22:

    As I said previously the first argument is an interface to your tank. This
    is a reference so the exact value of e.g. `tank.position` *will* change
    over time, but *only* when your generator is currently not executing.
    There are other attributes to this interface than your position but I
    haven't managed to write a full documentation just yet.

* Line 24-26

    It's getting a little bit more interesting now. We're setting the tank to
    full speed and rotate by -90°, i.e. to the top. After that we yield a
    function that will return `False` until the tank moved up so the y
    coordinate of its position is smaller 50. Keep in mind that for some stupid
    reason the origin is in the top left corner in computer graphics.
    This is the important step, until now our generator ran indisturbed and the
    value of `tank.position` didn't change (since it was the only thing
    running), now that we yielded the function the rest of the game will
    continue to run and 'wake' us when the condition encoded in the function is
    true.

* Line 29-40:

    Now those are some minor variations of the former theme, just to drive the
    point home.

* Line 42:

    Just something to ease debugging of your scripts, check
    [this](pytanks/scripts.py#L15) if you're familiar with python `logging`
    module.

* Line 44:

    It's getting a bit complicated here to show that the function we return
    don't have to be without side effects, but are actually a pretty good place
    to do some periodic stuff as it is called every tick of the game. Note that
    you don't have to use partial function application to pull this off, you can
    also use closures and nested function definitions to achieve the same, I
    just don't like it as much. You can also use sub-generators and the `yield from`
    syntax python provides. The `view.time` you see in there is a reference 
    to the total elapsed time in the course of the game, but it's one of the 
    more ugly parts and likely to change in the future, so I'd rather not spend 
    so much time on that.

You will notice that the tank also has a weapon and we will see in 
[examples/demo_turret.py](examples/demo_turret.py#L10) how to use it. I will also 
explain a bit more about the second argument the generator function is call with.

* Line 13:
    
    So this is where weapons come in. Your tank has a attribute `.mount` which
    is a list of all stuff mounted on top of it (only one weapon so far, but
    that may change in the future). The weapon has a very similar interface to
    the one of your tank, but obviously some attributes will be different or
    not existent (I may or may not provide full or incomplete documentation on
    interfaces later™). Examples of attributes are:  
    * .position: as the weapon may not be mounted in center of your tank  
    * .rotation: in which direction you're pointing the thing  
    * .reload_time: the time it takes to reload the weapon  
    * .till_reloaded: the time until you can fire the next time  
    * .shoot ():  

        this one's a method and will fire the weapon if possible,
        note that as 'time is frozen' when your generator is running, calling
        it twice will not shoot twice, the second call will fail to fire the
        weapon since it's not reloaded yet

* Line 15:

    This is line has to important points:  
    1. the second parameter `view` is an iterator over *all* entities in the
       game (including the your tank) represented by similar interfaces as your
       tank or your weapon, but in a read-only fashion (again, full docs later)  
    2. the interfaces act like dictionary storing some meta data about the
       entity in question, e.g. the "Class" key lets you distinguish between
       barriers, tanks, turret or bullets; if an entity is not tagged with a
       certain key it will raise a `KeyError` just like an ordinary dictionary  

The rest of the loop is pretty similiar to the first demo, so this will have to
be enough for now.
