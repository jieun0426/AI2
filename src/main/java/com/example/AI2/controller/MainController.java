package com.example.AI2.controller;

import com.example.AI2.dto.NumberPlateDTO;
import com.example.AI2.entity.*;
import com.example.AI2.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.text.DecimalFormat;
import java.util.List;

@Controller
public class MainController {
    @Autowired
    IrisRepository irisRepository;
    @Autowired
    HubRepository hubRepository;
    @Autowired
    LawRepository lawRepository;
    @Autowired
    JudgRepository judgRepository;

    String rootPath = new File("").getAbsolutePath();  // 현재 프로젝트 루트

    @GetMapping(value = {"/", "/main"})
    public String ss1(){
        return "/main";
    }

    @GetMapping("/suwon")
    public String ss2() throws IOException, InterruptedException {
        ProcessBuilder pb=new ProcessBuilder("python",
                "src/main/resources/scripts/suwon1.py");

        pb.redirectOutput(ProcessBuilder.Redirect.INHERIT); // 파이썬 stdout -> 자바 콘솔
        pb.redirectError(ProcessBuilder.Redirect.INHERIT);  // 파이썬 stderr -> 자바 콘솔

        Process process = pb.start();

        int exitCode = process.waitFor();

        return "/suwon";
    }

    @GetMapping("/suwon2")
    public String ss3() throws IOException, InterruptedException {
        ProcessBuilder pb=new ProcessBuilder("python",
                "src/main/resources/scripts/suwon1.py");

        pb.redirectOutput(ProcessBuilder.Redirect.INHERIT); // 파이썬 stdout -> 자바 콘솔
        pb.redirectError(ProcessBuilder.Redirect.INHERIT);  // 파이썬 stderr -> 자바 콘솔

        Process process = pb.start();

        int exitCode = process.waitFor();

        return "/suwon2";
    }

    @GetMapping("/iris")
    public String ss4(@RequestParam("value") String num) throws IOException {
        if(Integer.parseInt(num)>0){
            ProcessBuilder processBuilder=new ProcessBuilder("python",
                    "src/main/resources/scripts/iris1.py", num);
            Process process=processBuilder.start();

            BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream(), "utf-8"));

            StringBuilder output = new StringBuilder();
            String line;

            while((line=br.readLine())!=null){
                output.append(line);
            }
        }

        return "redirect:/irisview";
    }

    @GetMapping("/irisview")
    public String ss5(Model model){
        List<IrisEntity> list=irisRepository.findAll();
        model.addAttribute("list", list);

        return "/irisView";
    }

    @GetMapping("/robo1save")
    public String ss6() throws IOException, InterruptedException {
        ProcessBuilder processBuilder =
                new ProcessBuilder("python","src/main/resources/scripts/garbage1.py");

        processBuilder.redirectOutput(ProcessBuilder.Redirect.INHERIT);
        processBuilder.redirectError(ProcessBuilder.Redirect.INHERIT);

        Process process=processBuilder.start();
        int exitCode = process.waitFor();
        return "redirect:/robo1view";
    }

    @GetMapping("/robo1view")
    public String ss6_2(Model model) throws IOException {
        model.addAttribute("text","부유물 탐지 결과");
        model.addAttribute("video","output_detect_converted.mp4");
        return "/roboView";
    }

    @GetMapping("/robo2save")
    public String ss7() throws IOException, InterruptedException {
        ProcessBuilder processBuilder =
                new ProcessBuilder("python","src/main/resources/scripts/human1.py");

        processBuilder.redirectOutput(ProcessBuilder.Redirect.INHERIT);
        processBuilder.redirectError(ProcessBuilder.Redirect.INHERIT);

        Process process=processBuilder.start();
        int exitCode = process.waitFor();
        return "redirect:/robo2view";
    }

    @GetMapping("/robo2view")
    public String ss7_2(Model model) throws IOException {
        model.addAttribute("text","사람 인식 결과");
        model.addAttribute("video","output_seg_converted.mp4");
        return "/roboView";
    }

    @GetMapping("/robo3save")
    public String ss8() throws IOException, InterruptedException {
        ProcessBuilder processBuilder =
                new ProcessBuilder("python","src/main/resources/scripts/count1.py");

        processBuilder.redirectOutput(ProcessBuilder.Redirect.INHERIT);
        processBuilder.redirectError(ProcessBuilder.Redirect.INHERIT);

        processBuilder.redirectErrorStream(true);
        Process process = processBuilder.start();

        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line); // or logger.info(line);
        }
        int exitCode = process.waitFor();
        return "redirect:/robo3view";
    }

    @GetMapping("/robo3view")
    public String ss8_2(Model model) throws IOException {
        model.addAttribute("text","차량 탐지 결과");
        model.addAttribute("video","output_cnt_converted.mp4");
        return "/roboView";
    }

    @GetMapping("/robo4save")
    public String ss9() throws IOException, InterruptedException {
        ProcessBuilder processBuilder =
                new ProcessBuilder("python","src/main/resources/scripts/ski1.py");

        processBuilder.redirectOutput(ProcessBuilder.Redirect.INHERIT);
        processBuilder.redirectError(ProcessBuilder.Redirect.INHERIT);

        Process process=processBuilder.start();
        int exitCode = process.waitFor();
        return "redirect:/robo4view";
    }

    @GetMapping("/robo4view")
    public String ss9_2(Model model) throws IOException {
        model.addAttribute("text","모션 인식 학습 결과");
        model.addAttribute("video","output_pose_converted.mp4");
        return "/roboView";
    }

    @GetMapping("/search")
    public String ss12(Model model, @RequestParam(name = "page", defaultValue = "1") int page){
        int pageSize = 5;
        int start = (page - 1) * pageSize;
        int end = page * pageSize;

        List<HubEntity> list = hubRepository.findByPage(start, end);
        int totalRecords = hubRepository.countAll();
        int totalPages = (int) Math.ceil((double) totalRecords / pageSize);

        model.addAttribute("list", list);
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", totalPages);

        return "/hubSearch";
    }

    @GetMapping("/search2")
    public String ss13(@RequestParam String keyword, Model model, @RequestParam(name = "page", defaultValue = "1") int page){
        int pageSize = 5;
        int start = (page - 1) * pageSize;
        int end = page * pageSize;

        List<HubEntity> list = hubRepository.findKeywordByPage(start, end, keyword);
        int totalRecords = hubRepository.countByKeyword(keyword);
        int totalPages = (int) Math.ceil((double) totalRecords / pageSize);

        model.addAttribute("list", list);
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", totalPages);
        model.addAttribute("keyword",keyword);
        model.addAttribute("count",totalRecords);
        return "/hubSearch";
    }

    @GetMapping("/input")
    public String ss14(){
        return "hubInput";
    }

    @GetMapping("/input2")
    public String ss15(@RequestParam String keyword, Model model) throws IOException, InterruptedException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType("application/json; charset=UTF-8"));
        headers.set("Accept-Charset", "UTF-8");

        ProcessBuilder pb = new ProcessBuilder("python", "src/main/resources/scripts/pipeline.py",keyword);
        Process process= pb.start();

        BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream(), "utf-8"));
        String line;
        StringBuilder output = new StringBuilder();
        System.out.println(br);
        while ((line = br.readLine()) != null) {
            System.out.println("line = br.readLine()");
            output.append(line);
        }
        int exitCode = process.waitFor();
        System.out.println(output.toString());

        model.addAttribute("result", output);
        model.addAttribute("keyword", keyword);
        return "/hubInput";
    }

    @GetMapping("/lawlist")
    public String ss17(Model model){
        List<LawEntity> list = lawRepository.findAll();
        model.addAttribute("list", list);
        return "lawListView";
    }

    @GetMapping("/lawdetail")
    public String ss18(@RequestParam("num") Long num, Model model){
        LawEntity lawEntity = lawRepository.findById(num).orElse(null);
        String str=lawEntity.getSentences();
        str=str.substring(2, str.length() - 2);
        System.out.println("원본 문자열: [" + str + "]");
        String[] parts = str.split("', '");
        StringBuilder sb = new StringBuilder();
        for (String s : parts) {
            sb.append(s.trim().replace("\\n", "<br>")).append("<br>");
        }
        System.out.println(sb);
        lawEntity.setSentences(sb.toString());
        model.addAttribute("item", lawEntity);
        return "/lawDetailView";
    }

    @GetMapping("/judglist")
    public String ss19(Model model, @RequestParam(name = "page", defaultValue = "1") int page){
        int pageSize = 10;
        int start = (page - 1) * pageSize;
        int end = page * pageSize;

        List<JudgEntity> list = judgRepository.findByPage(start, end);
        int totalRecords = judgRepository.countAll();
        int totalPages = (int) Math.ceil((double) totalRecords / pageSize);

        model.addAttribute("list", list);
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", totalPages);
        return "/judgListView";
    }

    @GetMapping("/judgdetail")
    public String ss20(@RequestParam("doc_id") String doc_id, Model model){
        JudgEntity judgEntity = judgRepository.findById(doc_id).orElse(null);
        String str = "";
        try {
            str = judgEntity.getSentences();
        } catch (Exception e) {
            str = "";
        }

        str=str.substring(2, str.length() - 2);
        System.out.println("원본 문자열: [" + str + "]");
        String[] parts = str.split("', '");
        StringBuilder sb = new StringBuilder();
        for (String s : parts) {
            sb.append(s.trim().replace("\\n", "<br>")
                    .replace("', \"", "<br>")
                    .replace("\", '", "<br>")
                    .replace("\", \"", "<br>")
                    .replace("\\n", "<br>")
            ).append("<br>");
        }
        System.out.println(sb);

        model.addAttribute("item", judgEntity);
        model.addAttribute("sentencesHtml", sb.toString());
        return "/judgDetailView";
    }

    @GetMapping("/tts")
    public String tts(){
        return "/tts";
    }

    @GetMapping("/stt")
    public String stt(Model model){
        File file = new File(rootPath + "/data/temp_audio_file.wav");

        boolean fileExists = file.exists();

        if (fileExists) {
            boolean deleted = file.delete();
            if (!deleted) {
                System.out.println("파일 삭제 실패: " + file.getAbsolutePath());
                // 그래도 fileExists는 true 유지 (브라우저에 표시 안하도록)
            } else {
                fileExists = false; // 삭제 성공했으니 파일 없음
            }
        }

        model.addAttribute("fileExists", fileExists);
        return "/stt";
    }

    @PostMapping("/audio_upload")
    public String mp3_upload(@RequestParam("file") MultipartFile mf, Model model) throws IOException, InterruptedException {
        String originalFilename = mf.getOriginalFilename();
        boolean fileExists = true;
        if (originalFilename == null || originalFilename.isEmpty()) {
            fileExists = false;
            model.addAttribute("fileExists", fileExists);
            model.addAttribute("text", "파일이 선택되지 않았습니다.");
            return "/stt";
        }

        String ext = originalFilename.substring(originalFilename.lastIndexOf('.') + 1).toLowerCase();

        String targetPath;
        if (ext.equals("wav") || ext.equals("mp3")) {
            targetPath = rootPath + "/data/temp_audio_file." + ext;
            mf.transferTo(new File(targetPath));
        } else {
            model.addAttribute("fileExists", fileExists);
            model.addAttribute("text", "지원하지 않는 파일 형식입니다. MP3 또는 WAV만 업로드하세요.");
            return "/stt";
        }

        ProcessBuilder pb = new ProcessBuilder("python", "src/main/resources/scripts/stt1.py");
        Process process= pb.start();

        BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream(),"utf-8"));
        StringBuilder output = new StringBuilder();
        String line;

        while((line=br.readLine())!=null){
            output.append(line).append("\n");
        }

        int exitCode = process.waitFor();

        model.addAttribute("fileExists", fileExists);
        model.addAttribute("text", output.toString());
        return "/stt";
    }

    @GetMapping("/ad")
    public String ad() throws IOException {

        ProcessBuilder pb = new ProcessBuilder("python", "src/main/resources/scripts/ad1.py");
        Process process= pb.start();

        BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream(), "utf-8"));
        String line;
        StringBuilder output = new StringBuilder();
        System.out.println(br);
        while ((line = br.readLine()) != null) {
            System.out.println("line = br.readLine()");
            output.append(line);
        }

        return "/adView";
    }

    @GetMapping("/carnumber")
    public String carnumber(){
        return "/carnum";
    }

    NumberPlateDTO numberPlateDTO;

    @PostMapping("/carnum_upload")
    public String carnum_upload(MultipartFile file, Model model) throws IOException, InterruptedException {
        file.transferTo(new File(rootPath+"/data/temp_carnumber_image.jpg"));

        ProcessBuilder pb = new ProcessBuilder("python", "src/main/resources/scripts/car_number1.py");

        pb.redirectOutput(ProcessBuilder.Redirect.INHERIT);
        pb.redirectError(ProcessBuilder.Redirect.INHERIT);

        Process process= pb.start();
        int exitCode = process.waitFor();

        int retries = 0;
        while (numberPlateDTO == null && retries < 600) {
            Thread.sleep(100); // 100ms 기다리기
            retries++;
        }

        return "redirect:/carnumResult";
    }

    @PostMapping("/python/numberout")
    @ResponseBody
    public ResponseEntity<String> numberout(@RequestBody NumberPlateDTO data) {
        System.out.println("numberout 실행");
        // 모델에 저장 대신 redirect할 때 파라미터로 넘김
        this.numberPlateDTO=data;
        return ResponseEntity.ok("데이터 수신 완료");
    }

    @GetMapping("/carnumResult")
    public String showResult(Model model) {
        if (numberPlateDTO == null) {
            model.addAttribute("text", "결과 없음");
            model.addAttribute("prob", 0);
        } else {
            DecimalFormat df = new DecimalFormat("#.##");
            model.addAttribute("text", numberPlateDTO.getText());
            model.addAttribute("prob", df.format(numberPlateDTO.getProb()));
        }
        return "/carnumResult";
    }
}
