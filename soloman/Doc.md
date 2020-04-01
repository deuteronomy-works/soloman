# Controls

## Naming
All soloman controls should begin with an S e.g.: Button becomes SButton

## Colors and Styling
Use a seperate qml file to store all colors.

```Default colors``` - Use Qt's default colors.

## Properties

```bgcolor``` - it should be grouped in three states: primary, hover and click

```color``` - it should be grouped in three states: primary, hover and click

```icon_label_color``` - since IconLabel object type does not provide with NOTIFYable properties, this property is the only way to change the color of the IconLabel using dynamic means. It should be kept away from the user, as much as possible

```radius``` - most controls should be provided with a radius, just as rectangle has a radius
