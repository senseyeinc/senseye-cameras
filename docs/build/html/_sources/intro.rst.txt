Introduction
============

The senseye_cameras module is a generic camera interface written by SenseyeInc.

It allows Python developers to easily grab frames from multiple types of cameras and write them to disk.

Modules
============

:py:mod:`Input <senseye_cameras.input.input.Input>` objects obtain data from a data source, such as a usb camera, pylon camera, or video.

:py:mod:`Output <senseye_cameras.output.output.Output>` objects write data to a file, such as a raw video file or a compressed video file.

:py:mod:`Stream <senseye_cameras.stream.Stream>` objects link a single input and output.

Input Types
============

You can view the inputs senseye_cameras currently supports by looking the :py:meth:`create_input <senseye_cameras.input.input_factory.create_input>` function docs.

Using Inputs
============

Input objects obtain data from a data source. They can be created by using the :py:meth:`create_input <senseye_cameras.input.input_factory.create_input>` function.

All Inputs support the :py:meth:`open <senseye_cameras.input.input.Input.open>` and :py:meth:`read <senseye_cameras.input.input.Input.read>` functions.

The **open** function initializes the Input object.

The **read** function returns data from the Input in a tuple with the format: (**data**, **timestamp**).

    **data** is typically a numpy array obtained from the Input object.

    **timestamp** is a unix timestamp that records when the frame was obtained.




Here's a simple example that opens and reads from a usb camera.

.. literalinclude:: ../../examples/input/create_usb_input.py
    :language: python


More examples can be found in the senseye_cameras/examples/input folder.

Output Types
============

You can view the outputs senseye_cameras currently supports by looking the :py:meth:`create_output <senseye_cameras.output.output_factory.create_output>` function docs.


Using Outputs
==============

Output objects put data into a file. They can be created by using the :py:meth:`create_output <senseye_cameras.output.output_factory.create_output>` function.

All Outputs support the :py:meth:`write <senseye_cameras.output.output.Output.write>`, :py:meth:`close <senseye_cameras.output.output.Output.close>`, and :py:meth:`set_path <senseye_cameras.output.output.Output.set_path>` functions.

The **set_path** function takes in a path and tells the Output object where to write data to.

The **write** function writes data, typically in the form of numpy arrays, to the Output object.

The **close** function gracefully closes the Output object.

Here's a simple example that creates and writes to a raw Output object.

.. literalinclude:: ../../examples/output/create_raw_video_output.py
    :language: python


More examples can be found in the senseye_cameras/examples/output folder.

Streams
============

The :py:meth:`Stream <senseye_cameras.stream>` module is a high level module that links a single Input and Output.

Here's a simple example that creates a stream that uses a usb camera and writes to an avi file:

.. literalinclude:: ../../examples/stream/usb_to_avi.py
    :language: python

More examples can be found in the senseye_cameras/examples/stream folder.
