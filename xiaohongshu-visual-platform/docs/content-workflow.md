# Content Generation Workflow

## Overview

The content generation workflow has been optimized to include a review stage before image generation. This prevents wasting compute resources on images for content that may need to be regenerated or edited.

## Two-Stage Workflow

### Stage 1: Content Generation & Review

1. User enters topic in TopicInput component
2. System generates content (title, body, image descriptions)
3. ContentReviewPanel displays generated content for review
4. User has three options:
   - **Regenerate**: Start over with new content
   - **Edit**: Manually modify title and body
   - **Confirm**: Proceed to image generation

### Stage 2: Image Generation

1. User confirms content quality
2. System generates images based on prompts
3. ResultPreview displays final content with images
4. User can save, edit, or discard the complete content

## Components

### ContentReviewPanel

**Purpose**: Display generated content for user review before image generation

**Props**:
- `content` (Object): Generated content with title, body, and image descriptions
- `loading` (Boolean): Whether image generation is in progress

**Events**:
- `regenerate`: User wants to generate new content
- `edit`: User wants to manually edit content
- `confirm`: User confirms content and wants to generate images

**Features**:
- Displays title, body, and image descriptions
- Shows hint about avoiding compute waste
- Three action buttons with clear labels
- Disabled state during image generation

### ContentEditModal

**Purpose**: Allow manual editing of generated content

**Props**:
- `content` (Object): Content to edit (title and body)

**Events**:
- `close`: User cancels editing
- `save`: User saves edited content

**Features**:
- Modal overlay with centered content
- Form inputs for title and body
- Close button (×) in header
- Cancel and Save buttons in footer
- Click outside to close

## State Management

### CreateView State Variables

```javascript
// Existing state
const result = ref(null)              // Final content with images
const showProgress = ref(false)       // Progress modal visibility

// New state for two-stage workflow
const reviewStage = ref(false)        // Whether in review stage
const generatedContent = ref(null)    // Content awaiting review
const showEditModal = ref(false)      // Edit modal visibility
```

## User Flow

```
[Topic Input]
     ↓
[Generate Content]
     ↓
[Review Stage] ←──────┐
     ↓                │
  Regenerate ─────────┘
  Edit ──→ [Edit Modal] ──→ [Review Stage]
  Confirm
     ↓
[Generate Images]
     ↓
[Result Preview]
```

## Benefits

1. **Compute Savings**: Only generate images after content is approved
2. **Better UX**: User can review and edit before committing to image generation
3. **Flexibility**: Three options (regenerate/edit/confirm) give user control
4. **Clear Workflow**: Two distinct stages with clear transitions

## Technical Details

### Conditional Rendering

The CreateView template uses conditional rendering to show different components based on workflow stage:

```vue
<!-- Stage 1: Topic Input -->
<TopicInput v-if="!reviewStage && !result" />

<!-- Stage 2: Content Review -->
<ContentReviewPanel v-if="reviewStage" />

<!-- Stage 3: Edit Modal (overlay) -->
<ContentEditModal v-if="showEditModal" />

<!-- Stage 4: Result Preview -->
<ResultPreview v-if="result" />
```

### Handler Functions

- `handleGenerate`: Generates content only (no images)
- `handleConfirmContent`: Generates images after user confirms
- `handleRegenerateContent`: Resets to topic input stage
- `handleEditContent`: Opens edit modal
- `handleSaveEdit`: Saves edited content and closes modal

## Future Enhancements

Potential improvements for future iterations:

1. **Image Prompt Editing**: Allow editing individual image descriptions
2. **Partial Regeneration**: Regenerate only specific sections
3. **Content History**: Save and compare multiple content versions
4. **Auto-save**: Automatically save content drafts
5. **Batch Generation**: Generate multiple content variations at once
