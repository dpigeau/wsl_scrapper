SELECT * FROM {{ source('dev', 'heats') }} where total_score<0 or total_score>20