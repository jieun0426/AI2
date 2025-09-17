package com.example.AI2.dto;

import com.example.AI2.entity.LawEntity;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class LawDTO {
    long num;
    String statute_name;
    String effective_date;
    String proclamation_date;
    String statute_type;
    String statute_abbrv;
    String statute_category;
    String sentences;
    long data_class;

    public LawEntity entity(){
        return new LawEntity(null,statute_name,effective_date,proclamation_date,
                statute_type, statute_abbrv, statute_category, sentences, data_class);
    }
}
