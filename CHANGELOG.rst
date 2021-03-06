Changelog
=========

Release 2.0.0 (Development)
---------------------------

* Changed the convention on image masks to align with the scikit-image convention. Masks will be ``True`` for valid pixels, and ``False`` on invalid pixels.
* Broke off the ``skued.structure`` package into its own library, ``crystals``. The API is still provided under ``skued.structure`` for now.
* Added aspherical electron form factor parametrization from Zheng et al. 2009.
* Removed ``diff_register`` in favor of an analog of scikit-image's `register_translation`, `masked_register_translation`. 
* Removed `mnxc2` in favor of `mnxc`, the n-dimensional masked normalized cross-correlation.
* Removed `powder_center` due to unpredictable performance. Warnings will be issued on every function call. It will be removed in an upcoming release
* Removed `calibrate_scattvector`, which was deprecated.
* Removed `time_shift` and `time_shifts`, which were deprecated.

Release 1.0.1.0
---------------

* Added support for Gatan Digital Micrograph image formats DM3 and DM4
