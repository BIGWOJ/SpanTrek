# Migration Summary: CharField to ForeignKey for Landmark

## Changes Made to `create_landmark_lessons.py`

### 1. **Updated Import Statement**

```python
# OLD
from lessons.models import Lesson, Country

# NEW
from lessons.models import Lesson, Country, Landmark
```

### 2. **Updated Lesson Creation Logic**

**OLD Approach (CharField):**

```python
# Landmark was a simple string field
lesson, created = Lesson.objects.get_or_create(
    landmark=landmark,  # landmark was a string
    country=country_obj,
    order=lesson_data['order'],
    defaults=defaults
)
```

**NEW Approach (ForeignKey):**

```python
# Get or create the landmark object first
landmark_obj, landmark_created = Landmark.objects.get_or_create(
    name=landmark,
    country=country_obj,
    defaults={'adventure_order': 1}
)

# Then use the landmark object in lesson creation
lesson, created = Lesson.objects.get_or_create(
    landmark=landmark_obj,  # landmark is now a Landmark object
    order=lesson_data['order'],
    defaults={**defaults, 'country': country_obj}
)
```

### 3. **Updated Field Filtering**

```python
# OLD
defaults = {k: v for k, v in lesson_data.items() if k not in ['vocabularies', 'sentences', 'country']}

# NEW
defaults = {k: v for k, v in lesson_data.items() if k not in ['vocabularies', 'sentences', 'country', 'landmark']}
```

### 4. **Enhanced Update Logic**

Added proper handling for both country and landmark ForeignKey fields during updates:

```python
# Check if country needs updating
if lesson.country != country_obj:
    lesson.country = country_obj
    update_needed = True
```

## Benefits of This Migration

1. **Data Integrity**: Landmark is now properly normalized with its own model
2. **Relationships**: Landmarks are properly linked to their countries
3. **Extensibility**: Can add more landmark-specific fields (coordinates, description, etc.)
4. **Adventure Ordering**: Landmarks now have `adventure_order` for proper progression
5. **Query Efficiency**: Better database relationships and queries

## Files Updated

-   ✅ `lessons/management/commands/create_landmark_lessons.py`
-   ✅ No changes needed to `create_all_lessons.py` (it uses the updated command)

## Testing

Run the management command to test:

```bash
python manage.py create_landmark_lessons warsaw
```

The script will now:

1. Create the Landmark object if it doesn't exist
2. Link it properly to the Country
3. Create lessons with proper ForeignKey relationships
4. Handle updates correctly for both Country and Landmark fields
