select total_score
from {{ source('dev', 'heats') }}
where 
    total_score<0.0