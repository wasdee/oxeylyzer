# Thai Layout Optimization with Oxeylyzer

This guide explains how to use Oxeylyzer for Thai keyboard layout optimization.

## Setup

1. We've completed the following setup:
   - Created a Thai corpus configuration file in `static/corpus_configs/custom/thai.toml`
   - Generated Thai corpus data (with character, bigram, trigram frequencies) in `static/language_data_raw/thai.json`
   - Created Thai layout files in `static/layouts/thai/` (.kb format)
   - Added Thai to `languages_default.cfg`

## Using Oxeylyzer with Thai

1. Start Oxeylyzer:
   ```
   cargo run --release
   ```

2. Load the Thai corpus data:
   ```
   load thai
   ```
   This loads the Thai corpus data from `static/language_data_raw/thai.json`.

   > Note: Avoid using `--raw` flag when loading Thai. The `--raw` flag is meant for unprocessed text files, but we've already created a properly formatted JSON file with character frequencies.

3. Analyze a predefined Thai layout:
   ```
   use kedmanee
   ```
   This will use the standard Thai Kedmanee layout.

4. View statistics for this layout:
   ```
   stats
   ```
   This will show ergonomic metrics like finger usage, SFBs (same-finger bigrams), etc.

5. Generate an optimized layout based on Kedmanee:
   ```
   generate kedmanee 1000
   ```
   This will run 1000 iterations of optimization, starting from the Kedmanee layout.

6. Compare with other Thai layouts:
   ```
   use pattachote
   stats
   ```
   
   ```
   use manoonchai
   stats
   ```

7. You can pin certain keys if you want to preserve parts of a layout:
   ```
   use kedmanee
   pin ก จ 
   improve 500
   ```
   This would keep ก and จ in their original positions while optimizing the rest.

## Customizing Further

### Creating Your Own Thai Layout

1. Create a custom layout:
   ```
   use custom
   swap ก ข
   swap ค ช
   ```

2. Save your custom layout:
   ```
   save mylayout
   ```

3. Run optimization on your custom layout:
   ```
   improve 1000
   ```

### Visualizing Heatmaps

To better understand finger movement patterns and effort:
```
heatmap
```

## Key Thai Layout Considerations

1. **Consonant Frequency**: In Thai, some consonants like ก, ร, น are very common and should be placed on good positions.

2. **Vowel Placement**: Thai vowels (เ, า, ิ, ี, etc.) are used very frequently and should be easy to type.

3. **Tone Marks**: The four tone marks (่, ้, ๊, ๋) are critical and very common.

4. **Special Characters**: Certain special symbols like ๆ (mai yamok) and ฯ (pai-yan noi) are common and should be accessible.

## Thai Layout Ergonomic Goals

When optimizing a Thai layout, consider these goals:

1. Reduce same-finger bigrams (SFBs)
2. Balance hand usage (Thai traditionally has worse right-hand overload)
3. Optimize for common letter combinations
4. Place frequent characters on home row
5. Reduce finger travel distance

## Example Workflow for a New Thai Optimization Project

Here's a complete workflow for creating a new optimized Thai layout:

1. Start with existing layouts as baselines
2. Identify the strengths and weaknesses of each
3. Create a hybrid layout taking the best parts
4. Optimize with varying parameters
5. Test with real-world typing samples
6. Refine based on actual usage

## File Format Reference

The key files created for Thai layout optimization are:

1. `static/corpus_configs/custom/thai.toml` - Configuration for Thai character processing
2. `static/language_data_raw/thai.json` - Character, bigram and trigram frequencies
3. `static/layouts/thai/kedmanee.kb` - Kedmanee layout definition
4. `static/layouts/thai/pattachote.kb` - Pattachote layout definition
5. `static/layouts/thai/manoonchai.kb` - Manoonchai layout definition

By following this guide, you should be able to effectively use Oxeylyzer to analyze and optimize Thai keyboard layouts. 