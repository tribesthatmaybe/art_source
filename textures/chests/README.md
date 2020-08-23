# Chest textures

Some notes for future maintainers

#### Row 18 (and row 33)
Row 18 is the bottom row of pixels of the lid, _and_ when it is closed, it is
coplanar with row 33. For that reason, if both of these rows are not transparent, they should be identical \(or very very close) so as to avoid
[visible] z-fighting.

If you make either row transparent, there is some see-through when the chest
is opened. If you keep row 18 clear, it is through the top, 33 is on the bottom.

