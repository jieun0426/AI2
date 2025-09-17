package com.example.AI2.controller;

import com.example.AI2.dto.IrisDTO;
import com.example.AI2.dto.NumberPlateDTO;
import com.example.AI2.entity.IrisEntity;
import com.example.AI2.repository.IrisRepository;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.nio.charset.StandardCharsets;

@RestController
@RequestMapping(value="/python")
public class PythonController {
    @Autowired
    IrisRepository irisRepository;

    @PostMapping("/suwonout")
    public ResponseEntity<String> ss1(@RequestParam("bar_chart") MultipartFile barChartFile,
                                      @RequestParam("pie_chart") MultipartFile pieChartFile) throws IOException {

        // 저장 경로 설정
        String rootPath = new File("").getAbsolutePath();  // 현재 프로젝트 루트
        File dir = new File(rootPath + "/data");
        if (!dir.exists()) {
            dir.mkdirs(); // 디렉토리 없으면 생성
        }

        File barChartSaveFile = new File(dir, barChartFile.getOriginalFilename());
        barChartFile.transferTo(barChartSaveFile);

        File pieChartSaveFile = new File(dir, pieChartFile.getOriginalFilename());
        pieChartFile.transferTo(pieChartSaveFile);

        return ResponseEntity.ok("이미지 저장 성공");
    }

    @PostMapping("/irisout")
    public ResponseEntity<String> ss2(@RequestParam double loss,
                                      @RequestParam double accuracy,
                                      @RequestParam int epochs) throws IOException {

        IrisDTO irisDTO=new IrisDTO();
        irisDTO.setLoss(loss);
        irisDTO.setAccuracy(accuracy);
        irisDTO.setEpochs(epochs);

        System.out.println();
        System.out.println("iris 데이터: "+irisDTO.toString());
        System.out.println();

        IrisEntity irisEntity=irisDTO.entity();
        irisRepository.save(irisEntity);

        return ResponseEntity.ok("데이터 수신 완료");
    }

    @PostMapping("ttsin")
    @ResponseBody
    public ResponseEntity<String> ttsin(@RequestParam("txt") String txt) {
        try {
            String scriptPath = "src/main/resources/scripts/tts1.py";
            ProcessBuilder pb = new ProcessBuilder("python", scriptPath, txt);

            Process process = pb.start();

            BufferedReader stdOut = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8));
            BufferedReader stdErr = new BufferedReader(new InputStreamReader(process.getErrorStream(), StandardCharsets.UTF_8));

            String line;
            while ((line = stdOut.readLine()) != null) {
                System.out.println("PYTHON STDOUT ▶ " + line);
            }
            while ((line = stdErr.readLine()) != null) {
                System.err.println("PYTHON STDERR ▶ " + line);
            }

            int exitCode = process.waitFor();
            System.out.println("PYTHON 종료 코드 ▶ " + exitCode);
            Thread.sleep(200);

            if (exitCode == 0) {
                Thread.sleep(200);
                return ResponseEntity.ok("ok");
            } else {
                return ResponseEntity.status(500).body("python error");
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("exception");
        }
    }

}
