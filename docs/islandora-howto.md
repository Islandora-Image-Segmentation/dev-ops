---
title: Islandora development
theme: moon
---

# Developement environement

## Vagrant

- Easy way to manage virtual machines
- The `Vagrantfile` manages VM network and shared storage

```bash
vagrant up      # starts the vm
vagrant ssh     # ssh into the vm
vagrant halt    # shutsdown the machine
vagrant suspend # pauses the machine
vagrant resume  # brings the machine back from suspend  
```
## Vagrant continued
- The working directory is mapped to `/var/www/drupal/modules/all/Islandora-Image-Solution-Pack/`
- Islandora is available at localhost:8000
- Fedora and Solr at localhost:8080
- MySQL at localhost:3306
- If any of the ports are incorrect check the output of `vagrant up` for if any have changed.

## PhpStorm

- External Libraries
- External interpreter
- Drupal config
- Code style

## External Libraries
- Create a folder called `lib` outside of the git directory
- Clone Islandora, Drupal, tuque and the solution packs depencies into `lib`
```bash
islandora drupal tuque islandora_newspaper_batch islandora_ocr islandora_openseadragon islandora_paged_content islandora_solution_pack_large_image islandora_solution_pack_newspaper 
```
- [Add `lib` to the include path of PhpStorm](https://www.jetbrains.com/help/phpstorm/configuring-include-paths.html)
  * `ctrl+alt+s` to open settings
  * Languages & Frameworks $\rightarrow$ PHP
  * Include paths $\rightarrow$ `+`

## [External Interpreter](https://www.jetbrains.com/help/phpstorm/configuring-remote-interpreters.html)
- `ctrl+alt+s` to open settings
- Languages & Frameworks $\rightarrow$ PHP
- *CLI Interprepters* $\rightarrow$ `+`
- Select *vagrant*

## Drupal
- `ctrl+alt+s` to open settings
- Languages & Frameworks $\rightarrow$ PHP $\rightarrow$ Frameworks
- Drupal $\rightarrow$ Enable = True
- Drupal $\rightarrow$ Path = where you cloned Drupal
- Drupal $\rightarrow$ Version = 7

## Code Style
- `ctrl+alt+s` to open settings
- Editor $\rightarrow$ Code Style $\rightarrow$ PHP 
- Set from... $\rightarrow$ Drupal

## Drush
- A command-line utility for working with Drupal
- Should be run from the drupal directory

```bash
drush cc all # clears all cache
drush en module_name # enables a module
drush dis module_name # disables a module
```

## Enable Manually
- Browse to the instance
- Select Modules from the tool bar
- Find the module in the list, and enable
- Save configuration at the bottom of the page

# Basics

## Objects

- Stored in fedora repository
- Have Persistent Identifiers(PID)
- Have Datastreams
- Have [properties](https://github.com/Islandora/islandora/wiki/Working-With-Fedora-Objects-Programmatically-Via-Tuque#properties-1):
  * id (PID): of the form `namespace:id`
  * label
  * createdDate
  * owner
  * models

## Datastreams

- All Islandora objects have the `RELS-EXT` and `DC` datastreams
- Most have `OBJ` and `MODS` datastreams
- Datastreams have the following [properties](https://github.com/Islandora/islandora/wiki/Working-With-Fedora-Objects-Programmatically-Via-Tuque#properties-2):
  * id (DSID, "datastream ID")
  * label
  * checksum
  * content
  * mimetype
  * versionable

## [Tuque](https://github.com/Islandora/islandora/wiki/Working-With-Fedora-Objects-Programmatically-Via-Tuque)

- An API between PHP and Fedora
- Can be used to interact with Islandora objects

```php
$object = islandora_object_load($pid);
$label = $object->label;
$object->relationships = $relationships;
$datastream = $object[$dsid];
foreach ($object as $datastream) {
  $datastream->content = $my_new_content;
}
```


## Hooks

- Created by other modules
- Implemented by replacing `hook` with `my_module`
- Many can be found in [`islandora.api.php`]()

```php
hook_cool($foo){}

my_module_cool($foo){}

module_invoke_all('cool', 'bar');
```

## SOLR

I don't know much about it yet. But it's used for searching.

# Structure

## General
```shell
.
├── image_segmentation.info
├── image_segmentation.install
├── image_segmentation.module
├── includes
│   ├── admin.form.inc
│   └── derivatives.inc
├── LICENSE
├── README.md
├── theme
│   ├── image-segmentation-segment.tpl.php
│   └── theme.inc
└── xml
│  └── content_models
└── css
│  └── *.css
└── js
   └── *.js

```

## `module.info`

Gives information to drupal about the module.

```ini
name = Islandora Image Segmentation Solution Pack
description = "An Islandora module to handle segmented newspaper pages"
dependencies[] = islandora
dependencies[] = islandora_newspaper
package = Islandora Solution Packs
version = 7.x-dev
core = 7.x
```

## `module.install`

Implements install and uninstall hooks.

```php
function image_segmentation_install()
{
    module_load_include('inc', 'islandora', 'includes/solution_packs');
    islandora_install_solution_pack('image_segmentation');
}
```
```php
function image_segmentation_uninstall()
{
    module_load_include('inc', 'islandora', 'includes/solution_packs');
    islandora_install_solution_pack('image_segmentation', 'uninstall');
}
```

## `module.module`
- Implement your main Islandora hooks here
- These hooks will be covered in further detail later in the document
- Yes the names get redicuously long

```php
function image_segmentation_menu(){ ... }
function image_segmentation_theme($existing, $type, $theme, $path) { ... }
function image_segmentation_islandora_segmentedImageCModel_islandora_view_object(AbstractObject $object, $user, $page_number) { ... }
function image_segmentation_islandora_required_objects(IslandoraTuque $connection) { ... }
```

## `includes`
Put all your workers here

## `themes`
Put your templates and preprocessors

Put the required CSS and javascript files in `../css` and `../js`

# Menus

## `hook_menu()`

- Returns an array of menus;

```php
function image_segmentation_menu(){
  return array(
    'admin/islandora/segmentation' => array(
      'title' => 'Image Segmentaion Module',
      'description' => 'Configure the Image Segmentation solution pack.',
      'page callback' => 'drupal_get_form',
      'access arguments' => array('administer site configuration'),
      'page arguments' => array('image_segmentation_admin'),
      'file' => 'includes/admin.form.inc',
      'type' => MENU_NORMAL_ITEM,
    ),
  );
}
```

## Menu entry

- Each menu is a PHP array
- Keys are paths which can include wildcards
- Full documentation can be found [here](https://api.drupal.org/api/drupal/modules%21system%21system.api.php/function/hook_menu/7.x)

## Menu entry key-value pairs
  * `page callback`: the function to render the page
  * `page arguments`: an array of arguments sent to the callback
  * `access arguments`: passed to `access callback` to check for permission to use the menu. The callback defaults to 
  * `file`: to include, allows other code to be used to handle the callback
  * `type`: the type of menu to display

## Menu type

------------------------ -----------------------------
MENU_NORMAL_ITEM                          Regular menu
MENU_CALLBACK                            Non html menu
MENU_LOCAL_TASK            Typically shows up as a tab
MENU_DEFAULT_LOCAL_TASK    Shows up as the default tab
MENU_LOCAL_ACTION         Typically shows up as a link
------------------------ -----------------------------

## `drupal_get_form()`
- A function to create a form.
- Takes a form_id as an argument
- Must implement the `hook_form()` to use

```php
drupal_get_form('my_form');

function my_form(array $form, array $form_state) { ... }
```
## form

- Returns an array of form items

```php
function my_example_form($form, &$form_state) {
  $form['title'] = array(
        '#title' => t('Title'),
        '#type' => 'textfield',
        '#required' => FALSE,
        '#descritpion' => t('Title of the segment'),
        '#default_value' => isset($form_state['values']['title']) ? $form_state['values']['title'] : 'New Object',
    );
  $form['...'] = array( ... );
  ...
  return $form;
}
```

## Form validation and logic
- Hooks to validate and submit

```php
function my_example_form_validate($form, &$form_state) {
  // Validation logic.
}
```

```php
function my_example_form_submit($form, &$form_state) {
  // Submission logic.
}
```

## Some form item types

- textfield
- textarea
- managed_file
- Documentation [here](https://api.drupal.org/api/drupal/developer%21topics%21forms_api_reference.html/7.x)

## Config forms
- Return [`system_settings_from($from)`](https://api.drupal.org/api/drupal/modules!system!system.module/function/system_settings_form/7.x) to configure the system
  * Adds the submit button
  * Stores the variables with [`variable_set()`](https://api.drupal.org/api/drupal/includes%21bootstrap.inc/function/variable_set/7.x)
- Acces variables with [`variable_get()`](https://api.drupal.org/api/drupal/includes%21bootstrap.inc/function/variable_get/7.x)

```php
function my_settings_form(){
  $form = array(
    'max_size' = array(
      '#type' => 'textfield',
      '#title' => t('Maximium size'), ),);
  return system_settings_form($form);
} ...
$size = variable_get('max_size');
```

# Theming

## [`hook_theme()`](https://api.drupal.org/api/drupal/modules%21system%21system.api.php/function/hook_theme/7.x)

- Used to render an array as HTML
- Returns an array of theme items with the names of the themes

```php
function image_segmentation_theme($existing, $type, $theme, $path){
  return array(
    'image_segmentation_segment' => array(
      'file' => 'theme/theme.inc',
      'template' => 'theme/image-segmentation-segment',
      'pattern' => 'image_segmentation_sidebar__',
      'variables' => array('object' => NULL),
    )
  );
}
```

## Theme item values
- `file`: The file that implements the theme
- `template`: The name of the template without extension
- `variables`: An array of variables to be passed to the theme
  * The values get set when the theme is called

## `template_preprocess_hook()`

- Called before the theme is rendered
- Allows for the variables to be processed before rendering
- Accepts an array
- Returns the array that will be passed to the template 

## Preprocess example

```php
function template_preprocess_image_segmentation_segment(array &$variables) {
  $object = $variables['object'];
  if (isset($object['OBJ'])) {
    $obj_url = url("islandora/object/{$object->id}/datastream/OBJ/view");
    $params = array(
      'title' => $object->label,
      'path' => $obj_url,
    );
    $variables['segment'] = theme('image', $params);
  }
}
```

## Template
- Uses PHPTemplate by default
- Name it `my-template.tpl.php` in `theme/`

```php
<div class="image-segmentation-object islandora">
  <div><?php print $segment ?></div>
  <?php if (isset($object['OCR'])): ?>
      <div class="ocr content">
          <h2>OCR:</h2>
          <p><?php print $object['OCR']->content ?></p>
      </div>
  <?php endif; ?>
</div>
```

## Render an object
- Implement `hook_cmodelPid_islandora_view_object()`
- To use theme call `theme()`

```php
function my_module_islandora_myCmodel_islandora_view_object(
    AbstractObject $object, $user, $page_number)
{
  $output = theme(
    'image_segmentation_segment', 
    array('object' => $object));
  return array('' => $output);
}
```


# End

## Resources
- [How to make a solution pack](https://islandora.ca/sites/default/files/How%20to%20make%20a%20Solution%20Pack.pdf)
- [Islandora 101](https://github.com/Islandora-Labs/islandora_dev101)
- [Islandora and Tuque](https://github.com/Islandora/islandora/wiki/Working-With-Fedora-Objects-Programmatically-Via-Tuque)
- [Drupal 7 API](https://api.drupal.org/api/drupal/7.x)
- [Drupal 7 docs](https://www.drupal.org/docs/7)
